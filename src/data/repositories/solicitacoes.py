"""Solicitacoes de troca de senha contra o schema do portal."""
from __future__ import annotations

import psycopg
from psycopg_pool import PoolTimeout

from data.connection import conectar
from data.errors import BancoIndisponivel
from data.models import SolicitacaoSenha
from data.validacao import normalizar_email

HORAS_ATE_EXPIRAR = 24


def registrar_solicitacao_senha(email: str, nova_senha: str) -> bool:
    """Registra um pedido pendente para uma conta ativa.

    Devolve False quando o e-mail nao pertence a nenhuma conta ativa, sem
    registrar nada, para que a tela possa manter a mensagem neutra.
    """
    email_normalizado = normalizar_email(email)
    registrado = False

    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM usuario WHERE lower(email) = %s AND ativo = TRUE",
                    (email_normalizado,),
                )
                linha = cursor.fetchone()

                if linha is not None:
                    usuario_id = linha["id"]
                    cursor.execute(
                        """
                        DELETE FROM solicitacao_senha
                        WHERE usuario_id = %s AND situacao = 'pendente'
                        """,
                        (usuario_id,),
                    )
                    cursor.execute(
                        """
                        INSERT INTO solicitacao_senha (usuario_id, nova_senha)
                        VALUES (%s, %s)
                        """,
                        (usuario_id, nova_senha),
                    )
                    registrado = True

            conexao.commit()
    except (psycopg.OperationalError, PoolTimeout) as exc:
        raise BancoIndisponivel(
            "Nao foi possivel conectar ao banco de dados."
        ) from exc

    return registrado


def listar_solicitacoes_pendentes() -> list[SolicitacaoSenha]:
    """Marca as solicitacoes vencidas como expiradas e devolve as pendentes."""
    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE solicitacao_senha
                    SET situacao = 'expirada', decidido_em = NOW()
                    WHERE situacao = 'pendente'
                      AND criado_em < NOW() - INTERVAL '24 hours'
                    """
                )
                cursor.execute(
                    """
                    SELECT s.id, s.usuario_id, u.email, s.criado_em, s.situacao
                    FROM solicitacao_senha AS s
                    JOIN usuario AS u ON u.id = s.usuario_id
                    WHERE s.situacao = 'pendente'
                    ORDER BY s.criado_em
                    """
                )
                linhas = cursor.fetchall()
            conexao.commit()
    except (psycopg.OperationalError, PoolTimeout) as exc:
        raise BancoIndisponivel(
            "Nao foi possivel conectar ao banco de dados."
        ) from exc

    return [_para_solicitacao(linha) for linha in linhas]


def aprovar_solicitacao(solicitacao_id: int, administrador_id: int) -> bool:
    """Aprova um pedido pendente e aplica a senha solicitada.

    Devolve False quando o pedido ja havia sido decidido, sem alterar a senha.
    """
    aprovada = False

    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE solicitacao_senha
                    SET situacao = 'aprovada',
                        decidido_em = NOW(),
                        decidido_por = %s
                    WHERE id = %s AND situacao = 'pendente'
                    RETURNING usuario_id, nova_senha
                    """,
                    (administrador_id, solicitacao_id),
                )
                linha = cursor.fetchone()

                if linha is not None:
                    cursor.execute(
                        "UPDATE usuario SET senha = %s WHERE id = %s",
                        (linha["nova_senha"], linha["usuario_id"]),
                    )
                    aprovada = True

            conexao.commit()
    except (psycopg.OperationalError, PoolTimeout) as exc:
        raise BancoIndisponivel(
            "Nao foi possivel conectar ao banco de dados."
        ) from exc

    return aprovada


def recusar_solicitacao(solicitacao_id: int, administrador_id: int) -> bool:
    """Recusa um pedido pendente sem alterar a senha do usuario."""
    recusada = False

    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE solicitacao_senha
                    SET situacao = 'recusada',
                        decidido_em = NOW(),
                        decidido_por = %s
                    WHERE id = %s AND situacao = 'pendente'
                    """,
                    (administrador_id, solicitacao_id),
                )
                recusada = cursor.rowcount > 0

            conexao.commit()
    except (psycopg.OperationalError, PoolTimeout) as exc:
        raise BancoIndisponivel(
            "Nao foi possivel conectar ao banco de dados."
        ) from exc

    return recusada


def _para_solicitacao(linha: dict) -> SolicitacaoSenha:
    return SolicitacaoSenha(
        id=linha["id"],
        usuario_id=linha["usuario_id"],
        email=linha["email"],
        criado_em=linha["criado_em"],
        situacao=linha["situacao"],
    )
