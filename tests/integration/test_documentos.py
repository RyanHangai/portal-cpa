"""Testes da visibilidade de documentos."""
import pytest

from data.repositories.documentos import listar_para_perfis

pytestmark = pytest.mark.integration


def test_schema_atual_nao_possui_documentos():
    assert listar_para_perfis(["aluno"]) == []
