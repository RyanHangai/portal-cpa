"""Modelos de dominio do Portal CPA."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Usuario:
    id: int
    nome: str
    email: str
    ativo: bool
    perfis: tuple[str, ...]
    senha: str = ""


@dataclass(frozen=True)
class Dashboard:
    id: int
    nome: str
    url_embed: str
    ordem: int


@dataclass(frozen=True)
class Devolutiva:
    id: int
    area: str
    demanda: str
    resposta: str
    data_publicacao: date | None


@dataclass(frozen=True)
class Documento:
    id: int
    titulo: str
    categoria: str
    url_arquivo: str
    data_publicacao: date


@dataclass(frozen=True)
class CanalContato:
    id: int
    nome: str
    url: str
    ordem: int
