# Implementation Plan: Recuperação de Senha e Sessão Persistente

**Branch**: `003-recuperacao-senha-sessao` | **Date**: 2026-11-15 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-recuperacao-senha-sessao/spec.md`

## Summary

Permitir que qualquer usuário peça a troca da própria senha a partir da tela de login,
informando e-mail, nova senha e confirmação. O pedido fica pendente e só é aplicado
depois que um usuário com cargo Administrativo aprova; a recusa ou a expiração em 24
horas descartam o pedido sem alterar a senha.

Manter a sessão autenticada por 168 horas (uma semana) a partir de cada login, usando um
cookie assinado no navegador, de modo que recarregar a página ou reabrir o navegador não
exija novo login. A sessão é revalidada a cada carga da página, considerando o prazo e a
situação ativa do usuário.

## Technical Context

**Language/Version**: Python 3.14 (imagem do Compose)

**Primary Dependencies**: Streamlit, psycopg 3 e psycopg_pool (já existentes). Nenhuma
dependência nova: o cookie é lido de `st.context.cookies` e gravado com
`st.components.v1.html`, e a assinatura usa apenas a biblioteca padrão (`hmac`,
`hashlib`, `base64`, `json`).

**Storage**: PostgreSQL 18. Esta feature passa a usar uma tabela nova,
`solicitacao_senha`, e um tipo enumerado `situacao_solicitacao`, declarados em
`database/database.sql`, que continua sendo a única fonte do schema.

**Testing**: pytest (unidade e integração) e `streamlit.testing.v1.AppTest` para a tela de login.

**Target Platform**: Linux em Docker Compose; `http://localhost:8002`.

**Project Type**: aplicação web single-project com Streamlit.

**Performance Goals**: página renderizada em até 2 s; a restauração de sessão acrescenta uma
consulta ao banco por carga de página.

**Constraints**: sessão de 168 horas contadas de forma absoluta do login; troca de senha
somente após aprovação de Administrativo; nenhum envio de e-mail; cookie assinado e sem
senha; nenhuma tela exibe a senha; solicitações pendentes expiram em 24 horas.

**Scale/Scope**: instituição de pequeno porte; poucos usuários e solicitações de senha
pouco frequentes.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio | Como o plano atende |
|-----------|----------------------|
| I. Legibilidade acima de concisao | Módulos separados para token de sessão, solicitações e telas, com funções explícitas |
| II. Nomes descritivos | `registrar_solicitacao_senha`, `aprovar_solicitacao`, `ler_token_sessao` |
| III. Uma responsabilidade por funcao | Assinatura do token, persistência das solicitações, validação e interface em módulos distintos |
| IV. Fluxo explicito | Estados da solicitação e ordem de validação descritos em `data-model.md` |
| V. Consistencia | Segue `src/data/repositories`, `src/views` e `src/auth`; tabela nova no mesmo estilo do schema |
| Regras de estilo | Sem emojis em código, documentação e interface |
| Qualidade e revisao | Testes de unidade do token e das validações, integração do repositório e AppTest da tela de login |

Resultado: nenhuma violacao. A inclusao de uma tabela nova é uma mudança de schema
autorizada pela spec (premissa de armazenamento dos pedidos no servidor) e está
registrada em Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/003-recuperacao-senha-sessao/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── sessao-persistente.md
│   ├── data-access-solicitacoes.md
│   └── ui-recuperacao-senha.md
├── checklists/
│   └── requirements.md
└── spec.md
```

### Source Code (repository root)

```text
src/
├── auth/
│   ├── permissions.py          # inalterado
│   ├── service.py              # login, logout e integracao com o cookie
│   └── session.py              # NOVO: token assinado, leitura e validade da sessao
├── data/
│   ├── errors.py               # mantem as excecoes existentes
│   ├── models.py               # acrescenta SolicitacaoSenha
│   ├── validacao.py            # acrescenta validar_solicitacao_senha
│   └── repositories/
│       ├── usuarios.py         # acrescenta buscar_por_id
│       └── solicitacoes.py     # NOVO: registrar, listar, aprovar e recusar
├── views/
│   └── administracao.py        # secao de solicitacoes pendentes (Administrativo)
├── ui/
│   └── layout.py               # inalterado
└── main.py                     # opcao de recuperar senha e restauracao da sessao

tests/
├── unit/
│   ├── test_sessao_token.py    # NOVO
│   └── test_validacao_solicitacao.py  # NOVO
├── integration/
│   └── test_solicitacoes_senha.py     # NOVO
└── ui/
    └── test_login_recuperacao.py      # NOVO

database/
└── database.sql                # tipo situacao_solicitacao e tabela solicitacao_senha
```

**Structure Decision**: reaproveita a estrutura existente. A assinatura do cookie fica em
`src/auth/session.py`; as solicitações em `src/data/repositories/solicitacoes.py`; a
interface de recuperação na tela de login (`src/main.py`) e a de aprovação na página de
Administração (`src/views/administracao.py`).

## Complexity Tracking

| Item | Por que e necessario | Alternativa rejeitada |
|------|----------------------|-----------------------|
| Tabela `solicitacao_senha` | O pedido precisa sobreviver entre sessões para qualquer Administrativo decidir | Guardar o pedido apenas no navegador, que nenhum Administrativo veria |
| Guardar a senha pedida até a decisão | A aprovação aplica exatamente a senha escolhida pelo solicitante | Pedir a senha ao Administrativo na aprovação, expondo um valor que ele não deveria conhecer |
