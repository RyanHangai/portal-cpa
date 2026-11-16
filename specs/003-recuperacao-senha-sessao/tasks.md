# Tasks: Recuperação de Senha e Sessão Persistente

**Input**: Design documents from `/specs/003-recuperacao-senha-sessao/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: incluídos por decisão de plano (`pytest` e `AppTest` no Technical Context). Não há requisito de TDD.

**Organization**: tarefas agrupadas por user story para permitir implementação e teste independentes.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: pode rodar em paralelo (arquivos diferentes, sem dependências)
- **[Story]**: user story à qual a tarefa pertence (US1, US2, US3)
- Caminhos de arquivo exatos em todas as tarefas

## Path Conventions

- Projeto único: `src/` e `tests/` na raiz do repositório.
- Schema: `database/database.sql`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: preparação de dependência e schema para as histórias.

- [x] T001 [P] Manter as dependências existentes: ler o cookie em `st.context.cookies` e gravá-lo ou removê-lo com script em `st.components.v1.html`, sem nova dependência.
- [x] T002 Adicionar em `database/database.sql` o tipo `situacao_solicitacao` (`pendente`, `aprovada`, `recusada`, `expirada`), a tabela `solicitacao_senha` (`id` INTEGER identity como PK, `usuario_id` INTEGER NOT NULL com FK para `usuario.id`, `nova_senha` VARCHAR NOT NULL, `situacao` SITUACAO_SOLICITACAO NOT NULL DEFAULT 'pendente', `criado_em` TIMESTAMPTZ NOT NULL DEFAULT NOW(), `decidido_em` TIMESTAMPTZ, `decidido_por` INTEGER com FK para `usuario.id`) e o índice `idx_solicitacao_senha_situacao` em (`situacao`, `criado_em`).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: modelo e validação compartilhados por todas as histórias de recuperação.

**CRITICAL**: nenhuma user story começa antes desta fase terminar.

- [x] T003 [P] Adicionar a dataclass imutável `SolicitacaoSenha` (`id`, `usuario_id`, `email`, `criado_em`, `situacao`) em `src/data/models.py`, sem o campo `nova_senha`, para não expor a senha à interface.
- [x] T004 [P] Implementar `validar_solicitacao_senha(email, nova_senha, confirmacao)` em `src/data/validacao.py` com as regras: e-mail obrigatório; nova senha com no mínimo 8 caracteres (`TAMANHO_MINIMO_SENHA`); confirmação igual à nova senha.

**Checkpoint**: fundação pronta; as histórias podem começar.

---

## Phase 3: User Story 1 - Solicitar a troca e concluir com aprovação administrativa (Priority: P1) MVP

**Goal**: permitir que qualquer usuário registre um pedido de troca de senha e que um Administrativo o aprove, aplicando a nova senha.

**Independent Test**: registrar um pedido na tela de login e, como Administrativo, aprová-lo; confirmar que o login passa a valer com a senha nova e falha com a antiga.

### Tests for User Story 1

- [x] T005 [P] [US1] Teste unitário de `validar_solicitacao_senha` com dados válidos em `tests/unit/test_validacao_solicitacao.py`.
- [x] T006 [P] [US1] Teste de UI com `streamlit.testing.v1.AppTest` confirmando a opção de recuperação e os três campos na tela de login em `tests/ui/test_login_recuperacao.py`.
- [x] T007 [P] [US1] Teste de integração de `registrar_solicitacao_senha`, `aprovar_solicitacao` e login com a nova senha em `tests/integration/test_solicitacoes_senha.py`.

### Implementation for User Story 1

- [x] T008 [US1] Implementar `src/data/repositories/solicitacoes.py` com `registrar_solicitacao_senha(email, nova_senha) -> bool` (normaliza e-mail, exige conta ativa, apaga o pedido `pendente` anterior e insere o novo), `listar_solicitacoes_pendentes() -> list[SolicitacaoSenha]` (marca como `expirada` as pendentes com `criado_em` anterior a `NOW() - INTERVAL '24 hours'`), `aprovar_solicitacao(solicitacao_id, administrador_id) -> bool` (atualiza somente `situacao = 'pendente'`, grava `decidido_em` e `decidido_por`, aplica `nova_senha` em `usuario.senha` na mesma transação) e `recusar_solicitacao(solicitacao_id, administrador_id) -> bool` (atualiza somente `situacao = 'pendente'`, sem tocar em `usuario.senha`).
- [x] T009 [US1] Adicionar na barra lateral de login em `src/main.py` o expansor "Esqueci minha senha" com e-mail, nova senha, confirmação e o botão "Solicitar troca de senha", chamando `validar_solicitacao_senha` e `registrar_solicitacao_senha` e exibindo a mensagem neutra "Se os dados estiverem corretos, o pedido sera analisado por um Administrativo.".
- [x] T010 [US1] Adicionar em `src/views/administracao.py` a seção "Solicitações de senha" visível somente para o cargo `administrativo`, listando e-mail e momento de cada pedido pendente com os botões "Aprovar" e "Recusar", recarregando a lista e confirmando a decisão após cada ação.

**Checkpoint**: US1 funcional e testável de forma independente.

---

## Phase 4: User Story 2 - Permanecer logado por uma semana (Priority: P2)

**Goal**: manter a sessão do usuário por 168 horas a partir de cada login, sobrevivendo a recargas e à reabertura do navegador.

**Independent Test**: entrar no portal, recarregar a página e reabrir o navegador; confirmar que o usuário continua autenticado, que o cookie expira em 168 horas e que "Sair" o remove.

### Tests for User Story 2

- [x] T011 [P] [US2] Teste unitário de `criar_token_sessao` e `ler_token_sessao`, cobrindo token válido, token adulterado, token malformado e token com mais de 168 horas, em `tests/unit/test_sessao_token.py`.
- [x] T012 [P] [US2] Teste de integração de restauração de sessão com usuário ativo e com usuário inativo em `tests/integration/test_sessao_persistente.py`.

### Implementation for User Story 2

- [x] T013 [P] [US2] Adicionar a dataclass imutável `SessaoAutenticada` (`usuario_id`, `login_em`) em `src/data/models.py`.
- [x] T014 [US2] Implementar `src/auth/session.py` com `SESSAO_DURACAO_HORAS = 168`, `NOME_COOKIE_SESSAO = "portal_cpa_sessao"`, `criar_token_sessao(usuario_id, login_em)`, `ler_token_sessao(token)` e `sessao_expirada(login_em)`, usando payload JSON em base64url e assinatura HMAC-SHA256 com `cookie_secret()` e comparação por `hmac.compare_digest`.
- [x] T015 [US2] Adicionar `buscar_por_id(usuario_id)` em `src/data/repositories/usuarios.py` para a restauração da sessão.
- [x] T016 [US2] Integrar o cookie em `src/auth/service.py`: `entrar` cria o token e grava o cookie com validade de 168 horas; `sair` limpa o `st.session_state` e remove o cookie; `restaurar_sessao` valida o token, busca o usuário e recusa conta inexistente ou inativa.
- [x] T017 [US2] Restaurar a sessão em `src/main.py` antes de exibir o formulário de login, tolerando leitura vazia do cookie na primeira renderização sem tratar como sessão inválida.

**Checkpoint**: US1 e US2 funcionam de forma independente.

---

## Phase 5: User Story 3 - Recusar recuperações inválidas (Priority: P3)

**Goal**: recusar pedidos com dados inválidos com mensagens claras e sem alterar a senha.

**Independent Test**: enviar o formulário de recuperação com campos vazios, senha curta, confirmação divergente e e-mail inexistente, conferindo as mensagens e a ausência de solicitação criada.

### Tests for User Story 3

- [x] T018 [P] [US3] Testes unitários de cada regra de `validar_solicitacao_senha` (campo vazio, senha com 7 caracteres, confirmação divergente) em `tests/unit/test_validacao_solicitacao.py`.
- [x] T019 [P] [US3] Teste de integração de e-mail inexistente e de usuário inativo, confirmando que nenhuma solicitação é criada, em `tests/integration/test_solicitacoes_senha.py`.

### Implementation for User Story 3

- [x] T020 [US3] Exibir as mensagens específicas de campo obrigatório, senha mínima e confirmação divergente no formulário de recuperação em `src/main.py`, sem registrar pedido quando houver erro.

**Checkpoint**: todas as histórias funcionam de forma independente.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: documentação e validação final.

- [x] T021 [P] Atualizar `README.md` com o fluxo de recuperação de senha, a aprovação por Administrativo e a sessão de uma semana.
- [ ] T022 Executar os cenários de `quickstart.md` com Docker e registrar os resultados.
- [x] T023 Revisar `src/` e `tests/` para garantir ausência de emojis e confirmar que `database/database.sql` segue como única fonte do schema.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: sem dependências.
- **Foundational (Phase 2)**: depende da Fase 1 e bloqueia todas as histórias.
- **User Stories (Fases 3 a 5)**: dependem da Fase 2.
- **Polish (Fase 6)**: depende das histórias desejadas.

### User Story Dependencies

- **US1 (P1)**: depende de T002, T003 e T004; T008 depende de T002, T003 e T004; T009 e T010 dependem de T008.
- **US2 (P2)**: depende de T001 e T003; T014 depende de T003; T016 depende de T014 e T015; T017 depende de T014, T015 e T016.
- **US3 (P3)**: depende de T004 e T009.

### Within Each User Story

- Testes antes da implementação, falhando inicialmente.
- Repositório antes das telas.
- Telas antes da guarda de acesso final.

### Parallel Opportunities

- T001 e T002 em paralelo na Fase 1.
- T003 e T004 em paralelo na Fase 2.
- Todos os testes marcados [P] rodam em paralelo em cada história.
- US1, US2 e US3 podem rodar em paralelo depois da Fase 2 quando houver equipe.

---

## Parallel Example: User Story 1

```bash
Task: "Teste unitário de validar_solicitacao_senha em tests/unit/test_validacao_solicitacao.py"
Task: "Teste de UI com AppTest em tests/ui/test_login_recuperacao.py"
Task: "Teste de integração das solicitações em tests/integration/test_solicitacoes_senha.py"
```

---

## Implementation Strategy

### MVP First

1. Concluir a Fase 1 (Setup), incluindo a alteração de schema.
2. Concluir a Fase 2 (Foundational).
3. Concluir a US1 para ter o pedido e a aprovação funcionando.
4. Validar a US1 de forma independente com volume de banco recriado.

### Incremental Delivery

1. Setup e Foundational prontos.
2. US1 entrega a recuperação mediada.
3. US2 adiciona a sessão de uma semana.
4. US3 fecha as mensagens de recusa.
5. Cada história pode ser validada sem quebrar as anteriores.

### Parallel Team Strategy

1. Equipe conclui Setup e Foundational.
2. Depois da Fase 2: uma pessoa em US1, outra em US2 e outra em US3.

---

## Notes

- [P] indica tarefas sem dependência e em arquivos diferentes.
- O rótulo [Story] mantém a rastreabilidade com a especificação.
- A alteração de schema desta feature é a tabela `solicitacao_senha` e o tipo `situacao_solicitacao`; não há script de migração e o volume precisa ser recriado (`docker compose down -v`).
- A senha pedida é guardada em `solicitacao_senha.nova_senha` até a decisão e nunca é exibida na interface.
- O cookie `portal_cpa_sessao` não contém a senha e é assinado com `COOKIE_SECRET`.
- Verificar que os testes falham antes da implementação.

---

## Phase 7: Convergence

- [ ] T024 Descartar as solicitações pendentes de usuários inativos ao listar e recusar a aprovação quando a conta estiver inativa em `src/data/repositories/solicitacoes.py`, cumprindo a premissa de que contas desativadas têm pedidos descartados per Assumptions/Edge Cases (partial)
- [ ] T025 Exibir mensagem de campo obrigatório quando a nova senha ou a confirmação estiverem vazias, antes de avaliar tamanho e coincidência, em `src/data/validacao.py` e `src/main.py` per US3/AC1 (partial)
- [ ] T026 Adicionar teste de integração da expiração de 24 horas em `tests/integration/test_solicitacoes_senha.py`, gravando uma solicitação com `criado_em` no passado e conferindo que ela não aparece na listagem e não altera a senha per FR-021 (missing)
