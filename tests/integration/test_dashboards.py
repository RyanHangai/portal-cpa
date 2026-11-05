"""Testes de integracao da visibilidade de dashboards."""
import pytest

from data.repositories.dashboards import listar_para_perfis

pytestmark = pytest.mark.integration


def test_aluno_ve_dashboards_do_aluno():
    dashboards = listar_para_perfis(["aluno"])

    assert len(dashboards) >= 1
    assert all(dashboard.ordem >= 1 for dashboard in dashboards)


def test_perfil_sem_dashboard_nao_ve_nada():
    assert listar_para_perfis(["perfil-inexistente"]) == []
