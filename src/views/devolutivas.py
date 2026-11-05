"""Mural publico de devolutivas."""
from __future__ import annotations

import streamlit as st

from data.repositories.devolutivas import listar_publicadas
from ui.layout import mensagem_vazia


def render() -> None:
    st.subheader("Mural de devolutivas")
    devolutivas = listar_publicadas()

    if not devolutivas:
        mensagem_vazia("Nenhuma devolutiva publicada ate o momento.")
        return

    for devolutiva in devolutivas:
        titulo = devolutiva.area
        if devolutiva.data_publicacao is not None:
            titulo = f"{titulo} - {devolutiva.data_publicacao:%d/%m/%Y}"
        with st.expander(titulo):
            st.write("Demanda:", devolutiva.demanda)
            st.write("Resposta:", devolutiva.resposta)
