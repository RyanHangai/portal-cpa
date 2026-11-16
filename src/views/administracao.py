"""Pagina de administracao do portal."""
from __future__ import annotations

import streamlit as st

from auth.permissions import exigir_acesso, usuario_atual
from data.conteudo import CARGOS, CURSOS
from data.errors import DadosInvalidos, EmailDuplicado
from data.models import DadosCadastroUsuario
from data.repositories.usuarios import (
    buscar_por_email,
    criar_usuario_com_cargos,
    definir_senha,
    listar_ativos,
)
from data.validacao import validar_cadastro

PERFIS_GESTORES = ("administrativo", "coordenador")


def render() -> None:
    exigir_acesso(list(PERFIS_GESTORES))
    usuario = usuario_atual()
    st.subheader("Administracao")

    if "administrativo" in usuario.perfis:
        _formulario_criar_usuario()
        _formulario_redefinir_senha()
        _mostrar_base_bruta()
    else:
        st.info("Coordenador gerencia apenas o proprio curso nesta entrega.")


def _formulario_criar_usuario() -> None:
    st.subheader("Criar usuario")
    with st.form("criar_usuario"):
        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        cargos = st.multiselect("Cargos", CARGOS)
        curso = st.selectbox("Curso (obrigatorio para Aluno)", [""] + CURSOS)
        cpf = st.text_input(
            "CPF (opcional)",
            help="Pontos e traco sao removidos automaticamente.",
        )
        enviado = st.form_submit_button("Criar usuario")

    if not enviado:
        return

    dados = DadosCadastroUsuario(
        nome=nome,
        email=email,
        senha=senha,
        cargos=tuple(cargos),
        curso=curso or None,
        cpf=cpf or None,
    )

    erros = validar_cadastro(dados)
    if erros:
        for erro in erros:
            st.error(erro)
        return

    try:
        usuario = criar_usuario_com_cargos(dados)
    except EmailDuplicado:
        st.error("Ja existe usuario com este e-mail.")
    except DadosInvalidos as exc:
        st.error(str(exc))
    else:
        st.success(f"Usuario {usuario.nome} criado com sucesso.")


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
