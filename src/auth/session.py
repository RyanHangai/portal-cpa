"""Token assinado da sessao autenticada guardada no navegador."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone

from config import cookie_secret
from data.models import SessaoAutenticada

SESSAO_DURACAO_HORAS = 168
NOME_COOKIE_SESSAO = "portal_cpa_sessao"


def criar_token_sessao(usuario_id: int, login_em: datetime) -> str:
    """Monta o token assinado com o usuario e o momento do login."""
    conteudo = _codificar(
        {
            "usuario_id": usuario_id,
            "login_em": login_em.astimezone(timezone.utc).isoformat(),
        }
    )
    return f"{conteudo}.{_assinar(conteudo)}"


def ler_token_sessao(token: str | None) -> SessaoAutenticada | None:
    """Devolve a sessao quando o token for valido e estiver no prazo."""
    if not token or token.count(".") != 1:
        return None

    conteudo, assinatura = token.split(".")
    if not hmac.compare_digest(_assinar(conteudo), assinatura):
        return None

    dados = _decodificar(conteudo)
    if dados is None:
        return None

    try:
        usuario_id = int(dados["usuario_id"])
        login_em = datetime.fromisoformat(dados["login_em"])
    except (KeyError, TypeError, ValueError):
        return None

    if login_em.tzinfo is None:
        return None
    if sessao_expirada(login_em):
        return None

    return SessaoAutenticada(usuario_id=usuario_id, login_em=login_em)


def sessao_expirada(login_em: datetime) -> bool:
    """Indica se o prazo de 168 horas a partir do login ja passou."""
    agora = datetime.now(timezone.utc)
    return agora - login_em.astimezone(timezone.utc) >= timedelta(
        hours=SESSAO_DURACAO_HORAS
    )


def _codificar(dados: dict) -> str:
    bruto = json.dumps(dados).encode("utf-8")
    return base64.urlsafe_b64encode(bruto).decode("ascii").rstrip("=")


def _decodificar(conteudo: str) -> dict | None:
    preenchimento = "=" * (-len(conteudo) % 4)
    try:
        bruto = base64.urlsafe_b64decode(conteudo + preenchimento)
        dados = json.loads(bruto.decode("utf-8"))
    except (ValueError, TypeError):
        return None
    return dados if isinstance(dados, dict) else None


def _assinar(conteudo: str) -> str:
    assinatura = hmac.new(
        cookie_secret().encode("utf-8"),
        conteudo.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return base64.urlsafe_b64encode(assinatura).decode("ascii").rstrip("=")
