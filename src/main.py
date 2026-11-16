"""Ponto de entrada do Portal CPA."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

from auth.permissions import usuario_atual
from auth.service import aplicar_cookie_pendente, entrar, restaurar_sessao, sair
from data.errors import BancoIndisponivel
from data.repositories.solicitacoes import registrar_solicitacao_senha
from data.validacao import validar_solicitacao_senha
from ui.layout import cabecalho, configurar_pagina
from views import administracao, contato, dashboards, devolutivas, relatorios

PERFIS_ADMINISTRACAO = ("administrativo", "coordenador")
MENSAGEM_PEDIDO_ENVIADO = (
    "Se os dados estiverem corretos, o pedido sera analisado por um Administrativo."
)


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

    _formulario_recuperar_senha()


def _formulario_recuperar_senha() -> None:
    with st.sidebar.expander("Esqueci minha senha"):
        with st.form("recuperar_senha"):
            email = st.text_input("E-mail da conta")
            nova_senha = st.text_input("Nova senha", type="password")
            confirmacao = st.text_input("Confirmar nova senha", type="password")
            enviado = st.form_submit_button("Solicitar troca de senha")

        if not enviado:
            return

        erros = validar_solicitacao_senha(email, nova_senha, confirmacao)
        if erros:
            for erro in erros:
                st.error(erro)
            return

        try:
            registrar_solicitacao_senha(email, nova_senha)
        except BancoIndisponivel as exc:
            st.error(str(exc))
        else:
            # A mensagem e a mesma para e-mail existente e inexistente, para nao
            # revelar quais contas estao cadastradas.
            st.info(MENSAGEM_PEDIDO_ENVIADO)


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
    aplicar_cookie_pendente()

    usuario = usuario_atual()

    if usuario is None:
        usuario = restaurar_sessao()

    if usuario is None:
        _formulario_login()
    else:
        _botao_sair()

    cabecalho(usuario)
    st.navigation(_paginas(usuario)).run()


main()
