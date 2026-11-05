"""Ponto de entrada do Portal CPA."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

from auth.permissions import usuario_atual
from auth.service import entrar, sair
from ui.layout import cabecalho, configurar_pagina
from views import administracao, contato, dashboards, devolutivas, relatorios

PERFIS_ADMINISTRACAO = ("administrativo", "coordenador")


def _formulario_login() -> None:
    with st.sidebar.form("login"):
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        enviado = st.form_submit_button("Entrar")

    if enviado:
        usuario = entrar(email, senha)
        if usuario is None:
            st.sidebar.error("Credenciais invalidas.")
        else:
            st.rerun()


def _botao_sair() -> None:
    if st.sidebar.button("Sair"):
        sair()
        st.rerun()


def _paginas(usuario) -> list[st.Page]:
    paginas = []

    if usuario is not None:
        paginas.append(
            st.Page(dashboards.render, title="Dashboards", url_path="dashboards", default=True)
        )
        paginas.append(
            st.Page(relatorios.render, title="Relatorios", url_path="relatorios")
        )
        if set(usuario.perfis) & set(PERFIS_ADMINISTRACAO):
            paginas.append(
                st.Page(administracao.render, title="Administracao", url_path="administracao")
            )

    paginas.append(
        st.Page(
            devolutivas.render,
            title="Devolutivas",
            url_path="devolutivas",
            default=usuario is None,
        )
    )
    paginas.append(st.Page(contato.render, title="Contato", url_path="contato"))
    return paginas


def main() -> None:
    configurar_pagina()
    usuario = usuario_atual()

    if usuario is None:
        _formulario_login()
    else:
        _botao_sair()

    cabecalho(usuario)
    st.navigation(_paginas(usuario)).run()


main()
