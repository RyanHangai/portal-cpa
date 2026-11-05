# Implementation Plan: Portal de Transparência da CPA

**Branch**: `001-portal-cpa` | **Date**: 2026-11-04 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-portal-cpa/spec.md`

## Summary

Construir um portal web em Python com Streamlit, executado em Docker Compose, que
centraliza e apresenta, conforme o perfil do usuário, os dashboards de pesquisas
institucionais (incorporados a partir do Google Looker Studio), o mural público de
devolutivas, a área de relatórios e boletins e a página de contato. O controle de
acesso usa autenticação com e-mail e senha e perfis (Aluno, Professor, Coordenador,
Diretor, Administrativo e CPA Externo). Os dados persistem em PostgreSQL 18, também
no Compose, com volume nomeado.

A abordagem prioriza legibilidade: módulos pequenos e explícitos para autenticação,
permissões, acesso a dados e telas; SQL parametrizado organizado em repositórios;
sem truques nem otimizações prematuras, conforme a constituição do projeto.

## Technical Context

**Language/Version**: Python 3.14 (imagem `python:3.14` no Compose)

**Primary Dependencies**: Streamlit (interface), psycopg 3 (driver PostgreSQL),
bcrypt (hash de senha), streamlit-authenticator (login e cookie de sessão), PyJWT
(dependência do streamlit-authenticator), python-dotenv (configuração local)

**Storage**: PostgreSQL 18 (serviço `postgres` no Compose; volume nomeado
`postgres_data`; porta do host 8001; banco `postgres`)

**Testing**: pytest (unitário e integração), `streamlit.testing.v1.AppTest`
(fluxos de tela) e banco PostgreSQL descartável para integração

**Target Platform**: Linux em containers Docker Compose; acesso pelo navegador em
`http://localhost:8002`

**Project Type**: Aplicação web single-project (interface renderizada no servidor
mais banco de dados)

**Performance Goals**: renderizar cada página em até 2 s (excluindo o iframe externo
do dashboard); concluir login em até 30 s; suportar cerca de 500 usuários
simultâneos (porte da instituição)

**Constraints**: sessão válida por 168 horas; acesso à base bruta restrito a Diretor
e Administrativo; nenhum emoji em código, interface, comentários ou documentação;
comentários explicam o porquê, não o quê

**Scale/Scope**: 6 perfis, 5 áreas de conteúdo, cerca de 12 entidades; schema inicial
parcial em `database/database.sql` (a ser normalizado)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Princípio | Como o plano atende |
|-----------|----------------------|
| I. Legibilidade acima de concisão | Módulos curtos e explícitos; SQL legível; sem abstrações "espertas" |
| II. Nomes descritivos | Termos de domínio em português alinhados ao schema (usuario, devolutiva, perfil) |
| III. Uma responsabilidade por função | Separação em auth, permissions, repositórios, views e ui |
| IV. Fluxo explícito | Condicionais simples por perfil, sem metaprogramação |
| V. Consistência | Segue a estrutura existente (`src/`, `.docker/`, `database/`) |
| Regras de estilo | Sem emojis; comentários com o porquê; formatação consistente |
| Qualidade e revisão | Testes de unidade, integração e fluxo de tela |

Resultado: nenhuma violação. Nenhuma justificativa de complexidade necessária.

## Project Structure

### Documentation (this feature)

```text
specs/001-portal-cpa/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── ui-pages.md
│   └── data-access.md
├── checklists/
│   ├── requirements.md
│   └── security.md
├── tasks.md
└── spec.md
```

### Source Code (repository root)

```text
src/
├── main.py                  # porta de entrada: autenticação e navegação
├── config.py                # leitura de variáveis de ambiente
├── auth/
│   ├── service.py           # login, logout, hash de senha, sessão
│   └── permissions.py       # resolução de perfis e permissões
├── data/
│   ├── connection.py        # pool de conexões psycopg
│   ├── models.py            # dataclasses de domínio
│   └── repositories/
│       ├── usuarios.py
│       ├── dashboards.py
│       ├── devolutivas.py
│       ├── documentos.py
│       ├── contatos.py
│       └── eventos.py
├── views/
│   ├── dashboards.py
│   ├── devolutivas.py
│   ├── relatorios.py
│   ├── contato.py
│   └── administracao.py
└── ui/
    └── layout.py

tests/
├── unit/
├── integration/
└── ui/
```

**Structure Decision**: projeto único Streamlit. `src/main.py` concentra o gate de
autenticação e monta a navegação com `st.navigation`/`st.Page`, exibindo apenas as
páginas permitidas ao perfil. As telas ficam em `src/views/`, o acesso a dados em
`src/data/repositories/` e as regras de acesso em `src/auth/permissions.py`. Os
testes espelham as camadas.

## Complexity Tracking

> Sem violações constitucionais; seção não aplicável.
