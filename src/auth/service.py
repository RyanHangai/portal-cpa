"""Autenticacao de usuarios contra o schema existente."""
from __future__ import annotations

import json
from datetime import datetime, timezone

import streamlit as st
import streamlit.components.v1 as components

from auth.permissions import definir_usuario, limpar_usuario
from auth.session import (
    NOME_COOKIE_SESSAO,
    SESSAO_DURACAO_HORAS,
    criar_token_sessao,
    ler_token_sessao,
)
from data.models import Usuario
from data.repositories.usuarios import buscar_por_email, buscar_por_id

CHAVE_SESSAO_ENCERRADA = "sessao_encerrada"
CHAVE_COOKIE_PENDENTE = "cookie_sessao_pendente"
CHAVE_REMOCAO_COOKIE_PENDENTE = "cookie_sessao_remocao_pendente"


def senha_confere(senha: str, senha_armazenada: str) -> bool:
    return senha == senha_armazenada


def autenticar(email: str, senha: str) -> Usuario | None:
    usuario = buscar_por_email(email)
    if usuario is None or not usuario.ativo:
        return None
    if not senha_confere(senha, usuario.senha):
        return None
    return usuario


def entrar(email: str, senha: str) -> Usuario | None:
    usuario = autenticar(email, senha)
    if usuario is not None:
        definir_usuario(usuario)
        st.session_state.pop(CHAVE_SESSAO_ENCERRADA, None)
        st.session_state.pop(CHAVE_REMOCAO_COOKIE_PENDENTE, None)
        st.session_state[CHAVE_COOKIE_PENDENTE] = criar_token_sessao(
            usuario.id, datetime.now(timezone.utc)
        )
    return usuario


def sair() -> None:
    limpar_usuario()
    # O cookie do cabecalho continua visivel durante a sessao do navegador, por
    # isso o encerramento fica marcado ate um recarregamento completo da pagina.
    st.session_state[CHAVE_SESSAO_ENCERRADA] = True
    st.session_state.pop(CHAVE_COOKIE_PENDENTE, None)
    st.session_state[CHAVE_REMOCAO_COOKIE_PENDENTE] = True


def aplicar_cookie_pendente() -> None:
    """Grava ou remove o cookie da sessao depois de decidir a tela da execucao.

    A alteracao fica pendente por uma execucao porque um st.rerun imediato
    descarta o elemento que executa o script no navegador, e a gravacao se
    perderia.
    """
    token = st.session_state.pop(CHAVE_COOKIE_PENDENTE, None)
    if token is not None:
        _gravar_cookie_sessao(token)

    if st.session_state.pop(CHAVE_REMOCAO_COOKIE_PENDENTE, False):
        _remover_cookie_sessao()


def usuario_da_sessao(token: str | None) -> Usuario | None:
    """Resolve o usuario de um token valido, exigindo conta existente e ativa."""
    sessao = ler_token_sessao(token)
    if sessao is None:
        return None
    usuario = buscar_por_id(sessao.usuario_id)
    if usuario is None or not usuario.ativo:
        return None
    return usuario


def restaurar_sessao() -> Usuario | None:
    """Recupera a sessao guardada no cookie do navegador, quando existir."""
    if st.session_state.get(CHAVE_SESSAO_ENCERRADA):
        return None
    usuario = usuario_da_sessao(_ler_cookie_sessao())
    if usuario is None:
        return None
    definir_usuario(usuario)
    return usuario


def _ler_cookie_sessao() -> str | None:
    """Le o cookie direto do cabecalho da requisicao.

    A leitura sincrona garante que a sessao seja restaurada antes de montar a
    navegacao. Sem isso, a primeira renderizacao apos recarregar a pagina ainda
    enxerga o usuario como anonimo e a URL atual cai em "page not found".
    """
    contexto = getattr(st, "context", None)
    if contexto is None:
        return None
    try:
        return contexto.cookies.get(NOME_COOKIE_SESSAO)
    except Exception:
        return None


def _gravar_cookie_sessao(token: str) -> None:
    _executar_script_cookie(
        f"{NOME_COOKIE_SESSAO}={token}; path=/; "
        f"max-age={SESSAO_DURACAO_HORAS * 3600}; SameSite=Lax"
    )


def _remover_cookie_sessao() -> None:
    _executar_script_cookie(
        f"{NOME_COOKIE_SESSAO}=; path=/; max-age=0; SameSite=Lax"
    )


def _executar_script_cookie(instrucao: str) -> None:
    components.html(
        f"<script>document.cookie = {json.dumps(instrucao)};</script>",
        height=0,
    )
