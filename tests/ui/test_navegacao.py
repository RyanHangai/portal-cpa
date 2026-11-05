"""Testes de fluxo de tela com AppTest."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

pytestmark = pytest.mark.ui


def test_app_inicia_sem_excecao():
    caminho = Path(__file__).resolve().parents[2] / "src" / "main.py"
    app = AppTest.from_file(str(caminho), default_timeout=30)

    app.run()

    assert not app.exception
