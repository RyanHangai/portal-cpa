# Tasks: Cadastro de Usuário pelo Administrativo

**Input**: Design documents from `/specs/002-cadastro-usuario-admin/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: incluídos por decisão de plano (`pytest` e `AppTest` no Technical Context). Não há requisito de TDD.

**Organization**: tarefas agrupadas por user story para permitir implementação e teste independentes.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: pode rodar em paralelo (arquivos diferentes, sem dependências)
- **[Story]**: user story à qual a tarefa pertence (US1, US2, US3)
- Caminhos de arquivo exatos em todas as tarefas

## Path Conventions

- Projeto único: `src/` e `tests/` na raiz do repositório.
- Schema: `database/`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: preparação mínima para o cadastro.

- [x] T001 Alterar `usuario.cpf` para `VARCHAR(11)` em `database/database.sql`, normalizar o CPF em `src/data/validacao.py` (remover pontos e traço) e gravá-lo como texto no repositório.
- [x] T002 [P] Adicionar as constantes `CARGOS` e `CURSOS` em `src/data/conteudo.py` com os valores `aluno`, `coordenador`, `administrativo`, `cpa_externo` e os quatro cursos do enum.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: regras e persistência compartilhadas por todas as histórias.

**CRITICAL**: nenhuma user story começa antes desta fase terminar.

- [x] T003 Adicionar a dataclass `DadosCadastroUsuario` (nome, email, senha, cargos, curso, cpf) em `src/data/models.py`.
- [x] T004 [P] Criar as exceções `EmailDuplicado` e `DadosInvalidos` em `src/data/errors.py`.
- [x] T005 [P] Implementar `validar_cadastro(dados)` em `src/data/validacao.py` com as regras: nome, e-mail e senha obrigatórios; senha com no mínimo 8 caracteres; pelo menos um cargo válido; curso obrigatório quando Aluno; CPF opcional com 11 dígitos.
- [x] T006 Implementar `criar_usuario_com_cargos(dados)` em `src/data/repositories/usuarios.py` em transação única: verificar e-mail único, inserir `usuario` com `ativo = TRUE` e vincular cada cargo usando o `usuario.id` como id do perfil, na ordem definida em `research.md` R2.

**Checkpoint**: fundação pronta; as histórias podem começar.

---

## Phase 3: User Story 1 - Administrativo cria um novo usuário (Priority: P1)

**Goal**: permitir que o Administrativo cadastre um usuário com dados válidos e um ou mais cargos.

**Independent Test**: autenticar como Administrativo, cadastrar um usuário com cargo válido e confirmar que ele aparece na lista e consegue fazer login.

### Tests for User Story 1

- [x] T007 [P] [US1] Teste unitário de `validar_cadastro` com dados válidos em `tests/unit/test_cadastro_usuario.py`.
- [x] T008 [P] [US1] Teste de integração de `criar_usuario_com_cargos` criando usuário e vínculos em `tests/integration/test_cadastro_usuario.py`.

### Implementation for User Story 1

- [x] T009 [US1] Adicionar o formulário "Criar usuário" em `src/views/administracao.py` com nome, e-mail, senha, cargos (seleção múltipla), curso (quando Aluno) e CPF.
- [x] T010 [US1] Chamar `validar_cadastro` e `criar_usuario_com_cargos` no envio do formulário e exibir confirmação em `src/views/administracao.py`.
- [x] T011 [US1] Recarregar a lista de usuários após o cadastro em `src/views/administracao.py`.
- [x] T012 [US1] Verificar que o usuário criado autentica com o e-mail e a senha cadastrados, cobrindo com teste em `tests/integration/test_cadastro_usuario.py`.

**Checkpoint**: US1 funcional e testável de forma independente.

---

## Phase 4: User Story 2 - Validação dos dados de cadastro (Priority: P2)

**Goal**: recusar cadastros inválidos com mensagens claras.

**Independent Test**: enviar cadastros sem cargo, com campos vazios, senha curta, CPF inválido, Aluno sem curso e e-mail duplicado, conferindo as mensagens.

### Tests for User Story 2

- [x] T013 [P] [US2] Testes unitários de cada regra de `validar_cadastro` em `tests/unit/test_validacao_cadastro.py`.

### Implementation for User Story 2

- [x] T014 [US2] Exibir mensagens de erro para cargo ausente, campos obrigatórios, senha curta e CPF inválido em `src/views/administracao.py`.
- [x] T015 [US2] Tratar o erro `EmailDuplicado` com mensagem clara e sem criar usuário em `src/views/administracao.py`.
- [x] T016 [US2] Exigir curso quando Aluno estiver selecionado e exibir mensagem própria em `src/views/administracao.py`.

**Checkpoint**: US1 e US2 funcionam de forma independente.

---

## Phase 5: User Story 3 - Restrição de quem pode cadastrar (Priority: P3)

**Goal**: permitir o cadastro somente para Administrativo.

**Independent Test**: autenticar com Aluno, Coordenador e CPA Externo, conferir que a seção não aparece e que o acesso direto é negado.

### Tests for User Story 3

- [x] T017 [P] [US3] Teste unitário da guarda de Administrativo em `tests/unit/test_cadastro_permissao.py`.
- [x] T018 [P] [US3] Teste de UI da visibilidade do formulário em `tests/ui/test_cadastro_visibilidade.py`.

### Implementation for User Story 3

- [x] T019 [US3] Aplicar a guarda de acesso de Administrativo na seção de cadastro em `src/views/administracao.py` (a seção só é renderizada quando o perfil inclui `administrativo`).
- [x] T020 [US3] Ocultar a seção de cadastro para cargos diferentes de Administrativo em `src/views/administracao.py` (Coordenador mantém acesso à página, sem o formulário).

**Checkpoint**: todas as histórias funcionam de forma independente.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: documentação e validação final.

- [x] T021 [P] Atualizar `README.md` com o fluxo de criação de usuário.
- [ ] T022 [P] Executar os cenários de `quickstart.md` e registrar os resultados (requer Docker). Bloqueada: o Docker nao esta acessivel no ambiente atual (`/var/run/docker.sock` sem permissao).
- [x] T023 Revisar `src/` e `tests/` para garantir ausência de emojis e formatação consistente.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: sem dependências.
- **Foundational (Phase 2)**: depende da Fase 1 e bloqueia todas as histórias.
- **User Stories (Fases 3 a 5)**: dependem da Fase 2.
- **Polish (Fase 6)**: depende das histórias desejadas.

### User Story Dependencies

- **US1 (P1)**: começa após a Fase 2; depende de T003 a T006.
- **US2 (P2)**: depende de T005 e do formulário criado em US1 (T009).
- **US3 (P3)**: depende do formulário criado em US1 (T009).

### Within Each User Story

- Testes antes da implementação, falhando inicialmente.
- Validação e repositório (Fase 2) antes das telas.
- Telas antes do registro/guarda final.

### Parallel Opportunities

- T002 em paralelo na Fase 1.
- T004 e T005 em paralelo na Fase 2; T006 depende de T003, T004 e T005.
- Testes marcados [P] em cada história rodam em paralelo.
- US2 e US3 podem rodar em paralelo depois de T009.

---

## Parallel Example: User Story 1

```bash
Task: "Teste unitário de validar_cadastro com dados válidos em tests/unit/test_cadastro_usuario.py"
Task: "Teste de integração de criar_usuario_com_cargos em tests/integration/test_cadastro_usuario.py"
```

---

## Implementation Strategy

### MVP First

1. Concluir a Fase 1 (Setup).
2. Concluir a Fase 2 (Foundational).
3. Concluir a US1 para ter o cadastro funcionando com dados válidos.
4. Validar a US1 de forma independente.

### Incremental Delivery

1. Setup e Foundational prontos.
2. US1 entrega o cadastro básico.
3. US2 adiciona validações e mensagens.
4. US3 fecha o controle de acesso.
5. Cada história pode ser validada sem quebrar as anteriores.

### Parallel Team Strategy

1. Equipe conclui Setup e Foundational.
2. Depois da Fase 2: uma pessoa em US1, outra em US2 e outra em US3.

---

## Notes

- [P] indica tarefas sem dependência e em arquivos diferentes.
- O rótulo [Story] mantém a rastreabilidade com a especificação.
- Cada história deve ser concluída e testada de forma independente.
- Verificar que os testes falham antes da implementação.
- O schema muda apenas em `usuario.cpf`: `INTEGER` passa a `VARCHAR(11)`.
- `database/database.sql` e a unica fonte do schema; nao ha script de migracao. Bancos criados antes da alteracao precisam de volume novo (`docker compose down -v`).

---

## Phase 7: Convergence

- [x] T024 Normalizar o e-mail (remover espaços das pontas e converter para minúsculo) antes da checagem de duplicidade e do INSERT em `src/data/repositories/usuarios.py`, ajustando também `buscar_por_email` para comparar o valor normalizado per FR-007 e data-model (partial)
- [x] T025 Adicionar teste de UI com `streamlit.testing.v1.AppTest` em `tests/ui/test_cadastro_visibilidade.py` confirmando que o formulário de criar usuário não aparece para Coordenador, Aluno e CPA Externo per plan: Testing e T018 (partial)
- [x] T026 Implementar `BancoIndisponivel` em `src/data/errors.py` e traduzir falhas de conexão no cadastro, com mensagem amigável em `src/views/administracao.py` per contracts/data-access-cadastro.md (missing)
- [x] T027 Aplicar o mínimo de 8 caracteres também na redefinição de senha em `src/views/administracao.py`, reutilizando `TAMANHO_MINIMO_SENHA` de `src/data/validacao.py` per FR-008 (partial)
