"""Testes da matriz de permissoes por perfil."""
import pytest

from auth.permissions import PERFIS_VALIDOS, pode_acessar


@pytest.mark.parametrize("perfil", PERFIS_VALIDOS)
def test_cada_perfil_acessa_a_si_mesmo(perfil):
    assert pode_acessar((perfil,), [perfil]) is True


def test_aluno_nao_acessa_base_bruta():
    assert pode_acessar(("aluno",), ["administrativo"]) is False


def test_administrativo_acessa_base_bruta():
    assert pode_acessar(("administrativo",), ["administrativo"]) is True
