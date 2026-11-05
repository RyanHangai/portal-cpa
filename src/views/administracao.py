"""Pagina de administracao do portal."""
from __future__ import annotations

import streamlit as st

from auth.permissions import exigir_acesso, usuario_atual
from data.repositories.usuarios import buscar_por_email, definir_senha, listar_ativos

PERFIS_GESTORES = ("administrativo", "coordenador")


def render() -> None:
    exigir_acesso(list(PERFIS_GESTORES))
    usuario = usuario_atual()
    st.subheader("Administracao")

    if "administrativo" in usuario.perfis:
        _formulario_redefinir_senha()
        _mostrar_base_bruta()
    else:
        st.info("Coordenador gerencia apenas o proprio curso nesta entrega.")


def _formulario_redefinir_senha() -> None:
    with st.form("redefinir_senha"):
        email = st.text_input("E-mail do usuario")
        nova_senha = st.text_input("Nova senha", type="password")
        enviado = st.form_submit_button("Redefinir senha")

    if enviado and email and nova_senha:
        alvo = buscar_por_email(email)
        if alvo is None:
            st.error("Usuario nao encontrado.")
        else:
            definir_senha(alvo.id, nova_senha)
            st.success("Senha redefinida.")


def _mostrar_base_bruta() -> None:
    st.subheader("Base de dados bruta")
    usuarios = listar_ativos()
    st.dataframe(
        [
            {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "perfis": ", ".join(usuario.perfis),
            }
            for usuario in usuarios
        ]
    )
