# Implementation Plan: Cadastro de Usuário pelo Administrativo

**Branch**: `002-cadastro-usuario-admin` | **Date**: 2026-11-04 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-cadastro-usuario-admin/spec.md`

## Summary

Permitir que um usuario com cargo Administrativo cadastre novos usuarios informando
nome, e-mail, senha, um ou mais cargos e CPF opcional. O usuario nasce ativo e passa
a autenticar pelo login existente. Apenas o Administrativo ve e executa o cadastro.
O cadastro valida cargo obrigatorio, campos obrigatorios, e-mail unico na aplicacao,
senha minima e CPF com 11 digitos.

A gravacao acontece em uma unica transacao, criando o `usuario` e vinculando cada
cargo selecionado nas tabelas `aluno`, `coordenador`, `administrativo` e
`cpa_externo`, respeitando a direcao das chaves estrangeiras do schema atual.

## Technical Context

**Language/Version**: Python 3.14 (imagem do Compose)

**Primary Dependencies**: Streamlit (interface) e psycopg 3 (banco). Nenhuma
dependencia nova.

**Storage**: PostgreSQL 18, schema atual do DrawDB (`database/database.sql`).

**Testing**: pytest (unidade e integracao) e `streamlit.testing.v1.AppTest`.

**Target Platform**: Linux em Docker Compose; `http://localhost:8002`.

**Project Type**: aplicacao web single-project com Streamlit.

**Performance Goals**: cadastro concluido em menos de 2 minutos (SC-001); pagina
renderizada em ate 2 s.

**Constraints**: somente Administrativo cadastra; pelo menos um cargo obrigatorio;
e-mail unico verificado na aplicacao; senha minima de 8 caracteres; CPF opcional com
11 digitos; novo usuario sempre ativo; gravacao atomica.

**Scale/Scope**: instituicao de pequeno porte; cadastro manual de usuarios.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio | Como o plano atende |
|-----------|----------------------|
| I. Legibilidade acima de concisao | Uma funcao de criacao explicita, sem truques |
| II. Nomes descritivos | `criar_usuario_com_cargos`, `validar_cadastro` |
| III. Uma responsabilidade por funcao | Validacao, persistencia e interface separadas |
| IV. Fluxo explicito | Passos de insercao por cargo listados em ordem |
| V. Consistencia | Segue `src/data/repositories` e `src/views` |
| Regras de estilo | Sem emojis; comentarios com o porque |
| Qualidade e revisao | Testes de unidade, integracao e AppTest |

Resultado: nenhuma violacao.

## Project Structure

### Documentation (this feature)

```text
specs/002-cadastro-usuario-admin/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── ui-cadastro-usuario.md
│   └── data-access-cadastro.md
├── checklists/
│   └── requirements.md
└── spec.md
```

### Source Code (repository root)

```text
src/
├── data/
│   ├── conteudo.py                 # lista de cursos disponiveis
│   └── repositories/
│       └── usuarios.py             # criar_usuario_com_cargos
├── auth/
│   └── permissions.py              # guarda de Administrativo
├── views/
│   └── administracao.py            # formulario de cadastro
tests/
├── unit/
│   └── test_cadastro_usuario.py
└── integration/
    └── test_cadastro_usuario.py
```

**Structure Decision**: reaproveita a estrutura existente. A regra de negocio fica em
`src/data/repositories/usuarios.py`; a interface em `src/views/administracao.py`; as
validacoes puras em funcoes testaveis.

## Complexity Tracking

| Item | Por que e necessario | Alternativa rejeitada |
|------|----------------------|-----------------------|
| Insercao em varias tabelas por cargo | O schema separa os cargos em tabelas com FKs circulares | Nao existe coluna unica de cargo no schema |
| Campo `curso` no cadastro quando o cargo e Aluno | `aluno.curso` e NOT NULL no schema | Criar aluno sem curso viola o schema |
| Tipo da coluna `cpf` | `usuario.cpf` era INTEGER e nao comportava 11 digitos | Coluna alterada para `VARCHAR(11)` com autorizacao do usuario |
