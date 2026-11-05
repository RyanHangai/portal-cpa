"""Componentes de layout compartilhados."""
from __future__ import annotations

import streamlit as st

from data.models import Usuario


def configurar_pagina() -> None:
    st.set_page_config(page_title="Portal CPA", layout="wide")


def cabecalho(usuario: Usuario | None) -> None:
    st.title("Portal CPA")
    if usuario is not None:
        st.caption(f"{usuario.nome} - perfil: {', '.join(usuario.perfis)}")


def mensagem_vazia(texto: str) -> None:
    st.info(texto)
