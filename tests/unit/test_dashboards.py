"""Testes unitarios dos dashboards estaticos."""
from data.repositories.dashboards import listar_para_perfis


def test_aluno_ve_dashboards_do_aluno():
    resultado = listar_para_perfis(["aluno"])

    assert len(resultado) >= 2


def test_administrativo_ve_dashboard_da_administracao():
    resultado = listar_para_perfis(["administrativo"])
    nomes = [dashboard.nome for dashboard in resultado]

    assert "Pesquisa - Administracao" in nomes


def test_perfil_sem_dashboard_nao_ve_nada():
    assert listar_para_perfis([]) == []
