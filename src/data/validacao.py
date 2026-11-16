"""Validacoes puras do cadastro de usuario."""
from __future__ import annotations

from data.conteudo import CARGOS, CURSOS
from data.models import DadosCadastroUsuario

TAMANHO_MINIMO_SENHA = 8
TAMANHO_CPF = 11


def normalizar_cpf(cpf: str) -> str:
    """Remove pontos, tracos e espacos, mantendo apenas os digitos do CPF."""
    return "".join(caractere for caractere in cpf if caractere.isdigit())


def normalizar_email(email: str) -> str:
    """Remove espacos das pontas e converte o e-mail para minusculo."""
    return email.strip().lower()


def validar_cadastro(dados: DadosCadastroUsuario) -> list[str]:
    erros: list[str] = []

    if not dados.nome.strip():
        erros.append("Informe o nome.")
    if not dados.email.strip():
        erros.append("Informe o e-mail.")
    if len(dados.senha) < TAMANHO_MINIMO_SENHA:
        erros.append("A senha deve ter no minimo 8 caracteres.")
    if not dados.cargos:
        erros.append("Selecione pelo menos um cargo.")

    for cargo in dados.cargos:
        if cargo not in CARGOS:
            erros.append(f"Cargo invalido: {cargo}.")

    if "aluno" in dados.cargos and not dados.curso:
        erros.append("Informe o curso do aluno.")
    if dados.curso and dados.curso not in CURSOS:
        erros.append("Curso invalido.")

    if dados.cpf:
        digitos = normalizar_cpf(dados.cpf)
        if len(digitos) != TAMANHO_CPF:
            erros.append("O CPF deve ter 11 digitos.")

    return erros


def validar_solicitacao_senha(
    email: str,
    nova_senha: str,
    confirmacao: str,
) -> list[str]:
    erros: list[str] = []

    if not email.strip():
        erros.append("Informe o e-mail.")
    if len(nova_senha) < TAMANHO_MINIMO_SENHA:
        erros.append("A senha deve ter no minimo 8 caracteres.")
    if nova_senha != confirmacao:
        erros.append("A confirmacao deve ser igual a nova senha.")

    return erros
