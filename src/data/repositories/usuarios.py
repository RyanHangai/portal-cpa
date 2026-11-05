"""Consultas e comandos de usuario contra o schema existente."""
from __future__ import annotations

from data.connection import conectar
from data.models import Usuario

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
    consulta = f"SELECT {_COLUNAS} FROM usuario WHERE email = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(consulta, (email,))
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
