"""Pagina de relatorios e boletins."""
from __future__ import annotations

import streamlit as st

from auth.permissions import PERFIS_VALIDOS, exigir_acesso, usuario_atual
from data.repositories.documentos import listar_para_perfis
from ui.layout import mensagem_vazia


def render() -> None:
    exigir_acesso(list(PERFIS_VALIDOS))
    usuario = usuario_atual()
    documentos = listar_para_perfis(list(usuario.perfis))

    if not documentos:
        mensagem_vazia("Nenhum documento disponivel para o seu perfil.")
        return

    for documento in documentos:
        st.subheader(documento.titulo)
        st.caption(f"{documento.categoria} - {documento.data_publicacao:%d/%m/%Y}")
        st.markdown(f"[Abrir documento]({documento.url_arquivo})")
