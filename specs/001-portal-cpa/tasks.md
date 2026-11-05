# Tasks: Portal de Transparência da CPA

**Input**: Design documents from `/specs/001-portal-cpa/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: incluídos por decisão de plano (`pytest` e `AppTest` no Technical Context) e porque cada user story define um "Independent Test". Não há requisito de TDD.

**Organization**: tarefas agrupadas por user story para permitir implementação e teste independentes.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: pode rodar em paralelo (arquivos diferentes, sem dependências)
- **[Story]**: user story à qual a tarefa pertence (US1, US2, US3, US4, US5)
- Caminhos de arquivo exatos em todas as tarefas

## Path Conventions

- Projeto único: `src/` e `tests/` na raiz do repositório.
- Schema: `database/`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: inicialização do projeto e estrutura básica.

- [x] T001 Criar a estrutura de diretórios do projeto em `src/auth/`, `src/data/repositories/`, `src/views/`, `src/ui/`, `tests/unit/`, `tests/integration/` e `tests/ui/`.
- [x] T002 Adicionar dependências de execução em `requirements.txt`: `streamlit`, `psycopg[binary]`, `streamlit-authenticator` e `python-dotenv`.
- [x] T003 [P] Adicionar dependências de desenvolvimento em `requirements-dev.txt`: `pytest` e `pytest-cov`.
- [x] T004 [P] Criar `.env.example` com as chaves de conexão do banco e o segredo do cookie, e atualizar `.gitignore` para ignorar `.env`.
- [x] T005 [P] Remover o goose de `.docker/app.dev.dockerfile` e `.docker/app.init.dev.sh` e ajustar `compose.yaml` para montar `database.sql` e `seed.sql` em `/docker-entrypoint-initdb.d`, nesta ordem.
- [x] T006 [P] Criar `pytest.ini` na raiz com `testpaths = tests` e marcadores `unit`, `integration` e `ui`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: infraestrutura central que precisa existir antes de qualquer user story.

**CRITICAL**: nenhuma user story começa antes desta fase terminar.

- [x] T007 Normalizar `database/database.sql` conforme `data-model.md`: adicionar enum `perfil` com valores `aluno`, `professor`, `coordenador`, `diretor`, `administrativo`, `cpa_externo`; criar `usuario_perfil`; criar `professor` e `diretor`; adicionar `curso` em `coordenador`; remover as chaves circulares entre `usuario` e as tabelas de perfil.
- [x] T008 Adicionar em `database/database.sql` as tabelas de conteúdo `dashboard` (`ordem` e `ativo` obrigatórios), `dashboard_perfil`, `devolutiva` (`status` enum `rascunho`, `publicada`, `arquivada`), `documento` (`ativo` booleano), `documento_perfil`, `canal_contato` (`ordem`, `ativo`) e `evento_acesso`.
- [x] T009 [P] Criar `database/seed.sql` com os seis perfis, os quatro dashboards de `levantamento_requisitos/dashboard.md`, canais de contato, um usuário de exemplo por perfil, devolutivas publicadas de exemplo e documentos ativos de exemplo (um por categoria).
- [x] T010 Criar `src/config.py` lendo `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` e `COOKIE_SECRET` de variáveis de ambiente.
- [x] T011 Criar `src/data/connection.py` com o pool de conexões psycopg inicializado a partir de `src/config.py`.
- [x] T012 Criar `src/data/models.py` com dataclasses para `Usuario`, `Perfil`, `Dashboard`, `Devolutiva`, `Documento` e `CanalContato`.
- [x] T013 [P] Criar `src/data/repositories/usuarios.py` com `buscar_por_email` (e-mail único), `listar_por_perfil`, `criar_usuario` (senha sempre como hash bcrypt) e `definir_ativo`.
- [x] T014 [P] Criar `src/auth/permissions.py` com a matriz de permissões por perfil e funções auxiliares usadas por todas as views.
- [x] T015 Implementar `exigir_acesso(perfis_permitidos: list[str]) -> None` em `src/auth/permissions.py`, interrompendo a renderização e registrando o evento quando o perfil não tiver permissão.
- [x] T016 Criar `src/auth/service.py` com login, logout, verificação de senha com bcrypt e cookie de sessão com expiração de 168 horas.
- [x] T017 Criar `src/ui/layout.py` com cabeçalho, navegação e mensagens compartilhadas.
- [x] T018 Criar `src/main.py` com o gate de autenticação, `st.navigation`/`st.Page` e o direcionamento pós-login por perfil.

**Checkpoint**: fundação pronta; as user stories podem começar.

---

## Phase 3: User Story 1 - Acesso autenticado com direcionamento por perfil (Priority: P1)

**Goal**: permitir login e direcionar cada usuário para a página inicial do seu perfil.

**Independent Test**: autenticar com um usuário de cada perfil e confirmar o direcionamento e o bloqueio de páginas não permitidas.

### Tests for User Story 1

- [x] T019 [P] [US1] Testes unitários de resolução de perfis e negação de usuário inativo em `tests/unit/test_permissions.py`.
- [x] T020 [P] [US1] Teste de integração de login válido, credenciais inválidas e expiração de sessão em `tests/integration/test_login.py`.

### Implementation for User Story 1

- [x] T021 [US1] Implementar o formulário de login e as mensagens de erro em `src/main.py`.
- [x] T022 [US1] Implementar logout e tratamento de usuário inativo em `src/auth/service.py`.
- [x] T023 [US1] Implementar o redirecionamento pós-login por perfil em `src/main.py`.
- [x] T024 [US1] Implementar a expiração de sessão e o retorno ao login em `src/main.py`.

**Checkpoint**: US1 funcional e testável de forma independente.

---

## Phase 4: User Story 2 - Dashboards personalizados por perfil (Priority: P2)

**Goal**: exibir na página inicial apenas os dashboards permitidos ao perfil.

**Independent Test**: autenticar como Aluno, Coordenador e CPA Externo e confirmar que cada perfil vê somente os dashboards permitidos.

### Tests for User Story 2

- [x] T025 [P] [US2] Teste unitário do filtro de dashboards por perfil em `tests/unit/test_dashboards.py`.
- [x] T026 [P] [US2] Teste de integração da visibilidade de dashboards em `tests/integration/test_dashboards.py`.

### Implementation for User Story 2

- [x] T027 [P] [US2] Criar `src/data/repositories/dashboards.py` com `listar_para_perfis`, considerando `dashboard.ativo = true` e respeitando a coluna `ordem`.
- [x] T028 [US2] Criar `src/views/dashboards.py` exibindo os dashboards permitidos em iframe.
- [x] T029 [US2] Aplicar `exigir_acesso` no início de `src/views/dashboards.py` e validar o bloqueio de dashboard fora do perfil.
- [x] T030 [US2] Adicionar fallback com link direto e mensagem quando o embed do dashboard estiver indisponível em `src/views/dashboards.py`.
- [x] T031 [US2] Registrar a página de dashboards em `src/main.py` apenas para perfis autenticados.

**Checkpoint**: US1 e US2 funcionam de forma independente.

---

## Phase 5: User Story 3 - Mural de devolutivas público (Priority: P3)

**Goal**: publicar as devolutivas das áreas sem exigir login.

**Independent Test**: abrir o mural sem autenticação e confirmar que as devolutivas publicadas aparecem.

### Tests for User Story 3

- [x] T032 [P] [US3] Teste de integração da listagem pública de devolutivas em `tests/integration/test_devolutivas.py`.

### Implementation for User Story 3

- [x] T033 [P] [US3] Criar `src/data/repositories/devolutivas.py` com `listar_publicadas`, filtrando `status = publicada`.
- [x] T034 [US3] Criar `src/views/devolutivas.py` como página pública com estado vazio.
- [x] T035 [US3] Registrar a página pública de devolutivas em `src/main.py` sem exigir autenticação.

**Checkpoint**: US3 funcional de forma independente, inclusive sem login.

---

## Phase 6: User Story 4 - Área de relatórios e boletins (Priority: P4)

**Goal**: disponibilizar documentos institucionais conforme o perfil.

**Independent Test**: autenticar com perfis diferentes e confirmar que cada um vê apenas os documentos permitidos.

### Tests for User Story 4

- [x] T036 [P] [US4] Teste de integração da visibilidade de documentos por perfil em `tests/integration/test_documentos.py`.

### Implementation for User Story 4

- [x] T037 [P] [US4] Criar `src/data/repositories/documentos.py` com `listar_para_perfis`, considerando `documento.ativo = true`.
- [x] T038 [US4] Criar `src/views/relatorios.py` listando os documentos permitidos com ação de abrir e baixar.
- [x] T039 [US4] Aplicar `exigir_acesso` no início de `src/views/relatorios.py` e validar o bloqueio de documento fora do perfil.
- [x] T040 [US4] Tratar documentos inativos ou removidos em `src/views/relatorios.py`.
- [x] T041 [US4] Registrar a página de relatórios em `src/main.py` apenas para perfis autenticados.

**Checkpoint**: US4 funcional de forma independente.

---

## Phase 7: User Story 5 - Página de contato (Priority: P5)

**Goal**: disponibilizar os canais oficiais da CPA para a comunidade.

**Independent Test**: abrir a página sem autenticação e confirmar os atalhos e o destino de cada canal.

### Tests for User Story 5

- [x] T042 [P] [US5] Teste de integração da página pública de contato em `tests/integration/test_contato.py`.

### Implementation for User Story 5

- [x] T043 [P] [US5] Criar `src/data/repositories/contatos.py` com `listar_ativos`, respeitando a coluna `ordem`.
- [x] T044 [US5] Criar `src/views/contato.py` como página pública com os canais oficiais.
- [x] T045 [US5] Registrar a página pública de contato em `src/main.py`.

**Checkpoint**: todas as user stories funcionam de forma independente.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: melhorias que afetam várias histórias e requisitos transversais.

- [x] T046 [P] Criar `src/views/administracao.py` com gestão de usuários e de cursos (FR-011 e FR-012), com Administrativo e Diretor sem restrição de curso e Coordenador limitado ao próprio curso.
- [x] T047 Aplicar `exigir_acesso` também em `src/views/administracao.py` para os perfis Administrativo, Diretor e Coordenador restrito ao próprio curso.
- [x] T048 [P] Criar `src/data/repositories/eventos.py` e registrar eventos de acesso a conteúdo restrito (FR-013) em `src/auth/service.py`.
- [x] T049 Implementar a visão restrita da base de dados bruta apenas para Diretor e Administrativo em `src/views/administracao.py` (FR-006).
- [x] T050 Implementar o fluxo de recuperação de senha mediada por usuário de nível superior em `src/views/administracao.py` (FR-014).
- [x] T051 [P] Adicionar testes da matriz de permissões em `tests/unit/test_permissions_matrix.py`.
- [x] T052 Atualizar `README.md` com instruções de configuração, execução e validação.
- [ ] T053 Executar os cenários de `quickstart.md`, medir o tempo entre o login e a exibição do primeiro dashboard (SC-001) e registrar os resultados.
- [x] T054 Revisar `src/`, `tests/` e documentação para garantir ausência de emojis e formatação consistente.
- [x] T055 [P] Adicionar testes de fluxo de tela com `AppTest` em `tests/ui/test_navegacao.py`, cobrindo login, dashboards por perfil e páginas públicas.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: sem dependências.
- **Foundational (Phase 2)**: depende da Fase 1 e bloqueia todas as user stories.
- **User Stories (Fases 3 a 7)**: dependem da Fase 2.
- **Polish (Fase 8)**: depende das histórias desejadas.

### User Story Dependencies

- **US1 (P1)**: começa após a Fase 2; base de autenticação e direcionamento.
- **US2 (P2)**: depende de US1 para o acesso autenticado; filtragem de dashboards é independente.
- **US3 (P3)**: independente; página pública.
- **US4 (P4)**: depende de US1 para o acesso autenticado; visibilidade por perfil é independente.
- **US5 (P5)**: independente; página pública.

### Within Each User Story

- Testes antes da implementação, falhando inicialmente.
- Repositórios antes das views.
- Views antes do registro da página em `src/main.py`.

### Parallel Opportunities

- T003, T004, T005 e T006 em paralelo.
- T013, T014 e T009 em paralelo na Fase 2.
- US3 e US5 podem rodar em paralelo com US1/US2/US4.
- Testes marcados [P] em cada história rodam em paralelo.

---

## Parallel Example: User Story 2

```bash
Task: "Teste unitário do filtro de dashboards por perfil em tests/unit/test_dashboards.py"
Task: "Teste de integração da visibilidade de dashboards em tests/integration/test_dashboards.py"
Task: "Criar src/data/repositories/dashboards.py com listar_para_perfis"
```

---

## Implementation Strategy

### MVP First

1. Concluir a Fase 1 (Setup).
2. Concluir a Fase 2 (Foundational), que bloqueia todas as histórias.
3. Concluir a US1 para validar o gate de autenticação.
4. Validar a US1 de forma independente.

### Incremental Delivery

1. Setup e Foundational prontos.
2. US1 e US2 entregam o núcleo demonstrável do portal (login e dashboards por perfil).
3. US3, US4 e US5 agregam conteúdo público e documentação.
4. Cada história pode ser validada sem quebrar as anteriores.

### Parallel Team Strategy

1. Equipe conclui Setup e Foundational em conjunto.
2. Depois da Fase 2: uma pessoa em US1/US2, outra em US3/US5 e outra em US4.
3. Histórias integram de forma independente.

---

## Notes

- [P] indica tarefas sem dependência e em arquivos diferentes.
- O rótulo [Story] mantém a rastreabilidade com a especificação.
- Cada história deve ser concluída e testada de forma independente.
- Verificar que os testes falham antes da implementação.
- Evitar tarefas vagas, conflito no mesmo arquivo e dependências que quebrem a independência.
