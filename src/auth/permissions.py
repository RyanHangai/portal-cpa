"""Regras de perfil e controle de acesso."""
from __future__ import annotations

import streamlit as st

from data.models import Usuario

PERFIS_VALIDOS = (
    "aluno",
    "coordenador",
    "administrativo",
    "cpa_externo",
)

CHAVE_USUARIO = "usuario_autenticado"


def usuario_atual() -> Usuario | None:
    return st.session_state.get(CHAVE_USUARIO)


def definir_usuario(usuario: Usuario) -> None:
    st.session_state[CHAVE_USUARIO] = usuario


def limpar_usuario() -> None:
    st.session_state.pop(CHAVE_USUARIO, None)


def pode_acessar(perfis_usuario, perfis_permitidos) -> bool:
    if not perfis_permitidos:
        return True
    return bool(set(perfis_usuario) & set(perfis_permitidos))


def exigir_acesso(perfis_permitidos) -> None:
    usuario = usuario_atual()
    if usuario is None:
        st.warning("Faca login para acessar esta pagina.")
        st.stop()
    if not pode_acessar(usuario.perfis, perfis_permitidos):
        st.error("Seu perfil nao tem acesso a esta pagina.")
        st.stop()
