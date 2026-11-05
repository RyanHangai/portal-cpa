"""Pagina de dashboards por perfil."""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from auth.permissions import PERFIS_VALIDOS, exigir_acesso, usuario_atual
from data.repositories.dashboards import listar_para_perfis
from ui.layout import mensagem_vazia


def render() -> None:
    exigir_acesso(list(PERFIS_VALIDOS))
    usuario = usuario_atual()
    dashboards = listar_para_perfis(list(usuario.perfis))

    if not dashboards:
        mensagem_vazia("Nenhum dashboard disponivel para o seu perfil.")
        return

    for dashboard in dashboards:
        st.subheader(dashboard.nome)
        components.iframe(dashboard.url_embed, height=600, scrolling=True)
        st.markdown(f"[Abrir em nova aba]({dashboard.url_embed})")
