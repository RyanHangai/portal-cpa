"""Pagina de administracao do portal."""
from __future__ import annotations

import streamlit as st

from auth.permissions import exigir_acesso, usuario_atual
from data.conteudo import CARGOS, CURSOS
from data.errors import BancoIndisponivel, DadosInvalidos, EmailDuplicado
from data.models import DadosCadastroUsuario
from data.repositories.solicitacoes import (
    aprovar_solicitacao,
    listar_solicitacoes_pendentes,
    recusar_solicitacao,
)
from data.repositories.usuarios import (
    buscar_por_email,
    criar_usuario_com_cargos,
    definir_senha,
    listar_ativos,
)
from data.validacao import TAMANHO_MINIMO_SENHA, validar_cadastro

PERFIS_GESTORES = ("administrativo", "coordenador")
CHAVE_AVISO_SOLICITACAO = "aviso_solicitacao_senha"
MENSAGEM_SEM_SOLICITACOES = "Nao ha solicitacoes pendentes."


def render() -> None:
    exigir_acesso(list(PERFIS_GESTORES))
    usuario = usuario_atual()
    st.subheader("Administracao")

    if "administrativo" in usuario.perfis:
        _formulario_criar_usuario()
        _formulario_redefinir_senha()
        _secao_solicitacoes_senha(usuario)
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
    except BancoIndisponivel as exc:
        st.error(str(exc))
    else:
        st.success(f"Usuario {usuario.nome} criado com sucesso.")


def _formulario_redefinir_senha() -> None:
    with st.form("redefinir_senha"):
        email = st.text_input("E-mail do usuario")
        nova_senha = st.text_input("Nova senha", type="password")
        enviado = st.form_submit_button("Redefinir senha")

    if enviado and email and nova_senha:
        if len(nova_senha) < TAMANHO_MINIMO_SENHA:
            st.error("A senha deve ter no minimo 8 caracteres.")
            return
        alvo = buscar_por_email(email)
        if alvo is None:
            st.error("Usuario nao encontrado.")
        else:
            definir_senha(alvo.id, nova_senha)
            st.success("Senha redefinida.")


def _secao_solicitacoes_senha(usuario) -> None:
    st.subheader("Solicitacoes de senha")

    aviso = st.session_state.pop(CHAVE_AVISO_SOLICITACAO, None)
    if aviso:
        st.success(aviso)

    try:
        solicitacoes = listar_solicitacoes_pendentes()
    except BancoIndisponivel as exc:
        st.error(str(exc))
        return

    if not solicitacoes:
        st.info(MENSAGEM_SEM_SOLICITACOES)
        return

    for solicitacao in solicitacoes:
        colunas = st.columns([3, 2, 1, 1])
        colunas[0].write(solicitacao.email)
        colunas[1].write(solicitacao.criado_em.strftime("%d/%m/%Y %H:%M"))
        if colunas[2].button("Aprovar", key=f"aprovar_{solicitacao.id}"):
            _decidir_solicitacao(
                aprovar_solicitacao, "aprovada", solicitacao.id, usuario.id
            )
        if colunas[3].button("Recusar", key=f"recusar_{solicitacao.id}"):
            _decidir_solicitacao(
                recusar_solicitacao, "recusada", solicitacao.id, usuario.id
            )


def _decidir_solicitacao(
    decidir,
    resultado: str,
    solicitacao_id: int,
    administrador_id: int,
) -> None:
    try:
        decidida = decidir(solicitacao_id, administrador_id)
    except BancoIndisponivel as exc:
        st.error(str(exc))
        return

    if decidida:
        st.session_state[CHAVE_AVISO_SOLICITACAO] = f"Solicitacao {resultado}."
    else:
        st.session_state[CHAVE_AVISO_SOLICITACAO] = (
            "Esta solicitacao ja havia sido decidida."
        )
    st.rerun()


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
