"""Testes do mural de devolutivas."""
import pytest

from data.repositories.devolutivas import listar_publicadas

pytestmark = pytest.mark.integration


def test_schema_atual_nao_possui_devolutivas():
    assert listar_publicadas() == []
