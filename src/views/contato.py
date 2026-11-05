"""Pagina publica de contato."""
from __future__ import annotations

import streamlit as st

from data.repositories.contatos import listar_ativos
from ui.layout import mensagem_vazia


def render() -> None:
    st.subheader("Contato")
    canais = listar_ativos()

    if not canais:
        mensagem_vazia("Nenhum canal de contato disponivel.")
        return

    for canal in canais:
        st.markdown(f"[{canal.nome}]({canal.url})")
