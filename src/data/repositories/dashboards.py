"""Dashboards servidos a partir de conteudo estatico."""
from __future__ import annotations

from data.conteudo import DASHBOARDS
from data.models import Dashboard


def listar_para_perfis(perfis: list[str]) -> list[Dashboard]:
    selecionados = [
        item for item in DASHBOARDS if set(perfis) & set(item["perfis"])
    ]
    selecionados.sort(key=lambda item: item["ordem"])
    return [
        Dashboard(
            id=indice,
            nome=item["nome"],
            url_embed=item["url_embed"],
            ordem=item["ordem"],
        )
        for indice, item in enumerate(selecionados, start=1)
    ]
