"""Testes de login contra o schema existente."""
import pytest

from auth.service import autenticar

pytestmark = pytest.mark.integration


def test_usuario_inexistente_retorna_none():
    assert autenticar("naoexiste@exemplo.com", "qualquer") is None
