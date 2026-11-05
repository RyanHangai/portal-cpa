"""Canais de contato servidos a partir de conteudo estatico."""
from __future__ import annotations

from data.conteudo import CANAIS_CONTATO
from data.models import CanalContato


def listar_ativos() -> list[CanalContato]:
    return [
        CanalContato(
            id=indice,
            nome=canal["nome"],
            url=canal["url"],
            ordem=canal["ordem"],
        )
        for indice, canal in enumerate(CANAIS_CONTATO, start=1)
    ]
