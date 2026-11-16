"""Erros de dominio do cadastro de usuario."""
from __future__ import annotations


class DadosInvalidos(Exception):
    """Indica dados de cadastro invalidos."""


class EmailDuplicado(Exception):
    """Indica que ja existe usuario com o e-mail informado."""


class BancoIndisponivel(Exception):
    """Indica que nao foi possivel conectar ao banco de dados."""
