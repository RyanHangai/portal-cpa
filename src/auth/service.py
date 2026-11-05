"""Autenticacao de usuarios contra o schema existente."""
from __future__ import annotations

from auth.permissions import definir_usuario, limpar_usuario, usuario_atual
from data.models import Usuario
from data.repositories.usuarios import buscar_por_email


def senha_confere(senha: str, senha_armazenada: str) -> bool:
    return senha == senha_armazenada


def autenticar(email: str, senha: str) -> Usuario | None:
    usuario = buscar_por_email(email)
    if usuario is None or not usuario.ativo:
        return None
    if not senha_confere(senha, usuario.senha):
        return None
    return usuario


def entrar(email: str, senha: str) -> Usuario | None:
    usuario = autenticar(email, senha)
    if usuario is not None:
        definir_usuario(usuario)
    return usuario


def sair() -> None:
    limpar_usuario()
