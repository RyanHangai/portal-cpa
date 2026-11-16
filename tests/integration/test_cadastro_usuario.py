"""Testes de integracao do cadastro de usuario."""
import pytest

from auth.service import autenticar
from data.connection import conectar
from data.models import DadosCadastroUsuario
from data.repositories.usuarios import criar_usuario_com_cargos

pytestmark = pytest.mark.integration

EMAIL_TESTE = "coordenador.teste@exemplo.com"


def _limpar(email: str) -> None:
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT id FROM usuario WHERE email = %s", (email,))
            linha = cursor.fetchone()
            if linha is None:
                return
            usuario_id = linha["id"]
            cursor.execute("DELETE FROM coordenador WHERE id = %s", (usuario_id,))
            cursor.execute("DELETE FROM usuario WHERE id = %s", (usuario_id,))
        conexao.commit()


@pytest.fixture
def email_teste():
    _limpar(EMAIL_TESTE)
    yield EMAIL_TESTE
    _limpar(EMAIL_TESTE)


def test_criar_usuario_coordenador(email_teste):
    dados = DadosCadastroUsuario(
        nome="Coordenador Teste",
        email=email_teste,
        senha="senha123",
        cargos=("coordenador",),
        curso=None,
        cpf=None,
    )

    usuario = criar_usuario_com_cargos(dados)

    assert usuario.email == email_teste
    assert "coordenador" in usuario.perfis


def test_usuario_criado_consegue_autenticar(email_teste):
    dados = DadosCadastroUsuario(
        nome="Coordenador Teste",
        email=email_teste,
        senha="senha123",
        cargos=("coordenador",),
        curso=None,
        cpf=None,
    )
    criar_usuario_com_cargos(dados)

    autenticado = autenticar(email_teste, "senha123")

    assert autenticado is not None
    assert "coordenador" in autenticado.perfis


def test_cpf_e_gravado_apenas_com_digitos(email_teste):
    dados = DadosCadastroUsuario(
        nome="Coordenador Teste",
        email=email_teste,
        senha="senha123",
        cargos=("coordenador",),
        curso=None,
        cpf="123.456.789-01",
    )
    criar_usuario_com_cargos(dados)

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT cpf FROM usuario WHERE email = %s", (email_teste,))
            linha = cursor.fetchone()

    assert linha["cpf"] == "12345678901"
