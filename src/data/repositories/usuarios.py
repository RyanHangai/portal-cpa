"""Consultas e comandos de usuario contra o schema existente."""
from __future__ import annotations

import psycopg
from psycopg_pool import PoolTimeout

from data.connection import conectar
from data.errors import BancoIndisponivel, DadosInvalidos, EmailDuplicado
from data.models import DadosCadastroUsuario, Usuario
from data.validacao import normalizar_cpf, normalizar_email

_COLUNAS = """
    id, nome, email, senha, ativo, aluno_id, coordenador_id, admin_id, cpa_externo_id
"""

_PERFIS_POR_COLUNA = {
    "aluno_id": "aluno",
    "coordenador_id": "coordenador",
    "admin_id": "administrativo",
    "cpa_externo_id": "cpa_externo",
}


def _perfis(linha: dict) -> tuple[str, ...]:
    perfis = []
    for coluna, perfil in _PERFIS_POR_COLUNA.items():
        if linha.get(coluna) is not None:
            perfis.append(perfil)
    return tuple(perfis)


def _para_usuario(linha: dict) -> Usuario:
    return Usuario(
        id=linha["id"],
        nome=linha["nome"],
        email=linha["email"],
        ativo=linha["ativo"],
        perfis=_perfis(linha),
        senha=linha["senha"],
    )


def buscar_por_email(email: str) -> Usuario | None:
    consulta = f"SELECT {_COLUNAS} FROM usuario WHERE lower(email) = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(consulta, (normalizar_email(email),))
            linha = cursor.fetchone()
    return _para_usuario(linha) if linha else None


def buscar_por_id(usuario_id: int) -> Usuario | None:
    consulta = f"SELECT {_COLUNAS} FROM usuario WHERE id = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(consulta, (usuario_id,))
            linha = cursor.fetchone()
    return _para_usuario(linha) if linha else None


def listar_ativos() -> list[Usuario]:
    consulta = f"""
        SELECT {_COLUNAS}
        FROM usuario
        WHERE ativo = TRUE
        ORDER BY nome
    """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(consulta)
            linhas = cursor.fetchall()
    return [_para_usuario(linha) for linha in linhas]


def listar_por_perfil(perfil: str) -> list[Usuario]:
    coluna = _coluna_do_perfil(perfil)
    consulta = f"""
        SELECT {_COLUNAS}
        FROM usuario
        WHERE {coluna} IS NOT NULL
        ORDER BY nome
    """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(consulta)
            linhas = cursor.fetchall()
    return [_para_usuario(linha) for linha in linhas]


def definir_ativo(usuario_id: int, ativo: bool) -> None:
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                "UPDATE usuario SET ativo = %s WHERE id = %s",
                (ativo, usuario_id),
            )
        conexao.commit()


def definir_senha(usuario_id: int, senha: str) -> None:
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                "UPDATE usuario SET senha = %s WHERE id = %s",
                (senha, usuario_id),
            )
        conexao.commit()


def _coluna_do_perfil(perfil: str) -> str:
    colunas = {perfil: coluna for coluna, perfil in _PERFIS_POR_COLUNA.items()}
    return colunas[perfil]


def criar_usuario_com_cargos(dados: DadosCadastroUsuario) -> Usuario:
    email = normalizar_email(dados.email)
    cpf = normalizar_cpf(dados.cpf) if dados.cpf else None

    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM usuario WHERE lower(email) = %s",
                    (email,),
                )
                if cursor.fetchone() is not None:
                    raise EmailDuplicado(email)

                cursor.execute(
                    """
                    INSERT INTO usuario (nome, email, senha, ativo, cpf)
                    VALUES (%s, %s, %s, TRUE, %s)
                    RETURNING id
                    """,
                    (dados.nome, email, dados.senha, cpf),
                )

                usuario_id = cursor.fetchone()["id"]
                for cargo in dados.cargos:
                    _vincular_cargo(cursor, usuario_id, cargo, dados.curso)

            conexao.commit()
    except (psycopg.OperationalError, PoolTimeout) as exc:
        raise BancoIndisponivel(
            "Nao foi possivel conectar ao banco de dados."
        ) from exc

    return Usuario(
        id=usuario_id,
        nome=dados.nome,
        email=email,
        ativo=True,
        perfis=tuple(dados.cargos),
        senha=dados.senha,
    )


def _vincular_cargo(cursor, usuario_id: int, cargo: str, curso: str | None) -> None:
    if cargo == "administrativo":
        cursor.execute(
            "UPDATE usuario SET admin_id = %s WHERE id = %s",
            (usuario_id, usuario_id),
        )
        cursor.execute("INSERT INTO administrativo (id) VALUES (%s)", (usuario_id,))
    elif cargo == "coordenador":
        cursor.execute(
            "UPDATE usuario SET coordenador_id = %s WHERE id = %s",
            (usuario_id, usuario_id),
        )
        cursor.execute("INSERT INTO coordenador (id) VALUES (%s)", (usuario_id,))
    elif cargo == "aluno":
        if not curso:
            raise DadosInvalidos("Informe o curso do aluno.")
        cursor.execute(
            "UPDATE usuario SET aluno_id = %s WHERE id = %s",
            (usuario_id, usuario_id),
        )
        cursor.execute(
            "INSERT INTO aluno (id, curso) VALUES (%s, %s)",
            (usuario_id, curso),
        )
    elif cargo == "cpa_externo":
        cursor.execute("INSERT INTO cpa_externo (id) VALUES (%s)", (usuario_id,))
        cursor.execute(
            "UPDATE usuario SET cpa_externo_id = %s WHERE id = %s",
            (usuario_id, usuario_id),
        )
    else:
        raise DadosInvalidos(f"Cargo invalido: {cargo}.")
