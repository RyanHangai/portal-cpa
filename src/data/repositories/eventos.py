"""Auditoria: o schema atual nao possui tabela de eventos."""
from __future__ import annotations


def registrar_evento(
    usuario_id: int | None,
    recurso: str,
    acao: str,
    resultado: str = "permitido",
) -> None:
    return None
