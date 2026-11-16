# Contract: Sessão Persistente

## Cookie

| Item | Valor |
|------|-------|
| Nome | `portal_cpa_sessao` |
| Conteúdo | `<payload_base64url>.<assinatura_base64url>` |
| Validade | 168 horas a partir do login |
| Path | `/` |
| SameSite | `Lax` |

O conteúdo nunca inclui a senha.

## Payload

```json
{"usuario_id": 12, "login_em": "2026-11-15T18:30:00+00:00"}
```

Assinatura: HMAC-SHA256 do payload codificado, com `cookie_secret()`.

## Módulo `src/auth/session.py`

- `SESSAO_DURACAO_HORAS: int = 168`
- `NOME_COOKIE_SESSAO: str = "portal_cpa_sessao"`
- `criar_token_sessao(usuario_id: int, login_em: datetime) -> str`
  - Devolve o token assinado do exemplo acima.
- `ler_token_sessao(token: str | None) -> SessaoAutenticada | None`
  - Devolve `None` quando o token estiver ausente, malformado, com assinatura inválida ou
    com `login_em` há mais de 168 horas.
- `sessao_expirada(login_em: datetime) -> bool`
  - Compara com o horário atual em UTC.

## Uso em `src/auth/service.py`

- `entrar(email, senha)` deve, após autenticar, criar o token e gravar o cookie.
- `sair()` deve limpar `st.session_state` e remover o cookie.
- `restaurar_sessao(token)` deve:
  1. ler e validar o token;
  2. buscar o usuário por id;
  3. recusar quando o usuário não existir ou estiver inativo;
  4. devolver o `Usuario` e preencher `st.session_state`.

## Regras

- Sessão inválida é tratada como não autenticada, nunca como erro na tela.
- Cada login grava um token novo, reiniciando as 168 horas.
- O cookie é removido no logout, mesmo que o token ainda esteja no prazo.
- Se a leitura do cookie retornar vazio na primeira renderização, a página segue como não
  autenticada e tenta novamente na renderização seguinte.
