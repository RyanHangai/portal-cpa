"""Testes unitarios das regras de permissao."""
from auth.permissions import pode_acessar


def test_permissao_liberada_quando_perfil_esta_na_lista():
    assert pode_acessar(("aluno",), ["aluno", "coordenador"]) is True


def test_permissao_negada_quando_perfil_nao_esta_na_lista():
    assert pode_acessar(("aluno",), ["administrativo"]) is False


def test_lista_vazia_libera_qualquer_perfil_autenticado():
    assert pode_acessar(("aluno",), []) is True


def test_multiplos_perfis_usam_uniao():
    assert pode_acessar(("aluno", "coordenador"), ["coordenador"]) is True
