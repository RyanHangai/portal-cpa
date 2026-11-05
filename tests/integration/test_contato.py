"""Testes de integracao da pagina de contato."""
import pytest

from data.repositories.contatos import listar_ativos

pytestmark = pytest.mark.integration


def test_canais_ativos_disponiveis():
    canais = listar_ativos()

    assert len(canais) >= 1
    assert all(canal.url.startswith("http") for canal in canais)
