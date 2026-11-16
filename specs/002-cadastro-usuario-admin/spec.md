# Feature Specification: Cadastro de Usuário pelo Administrativo

**Feature Branch**: `002-cadastro-usuario-admin`

**Created**: 2026-11-04

**Status**: Draft

**Input**: User description: "Criação de um perfil novo, onde quem pode criar um perfil é somente o usuário com cargo de administrativo. O usuário com cargo de administrativo pode criar um usuário de qualquer cargo, atribuir uma senha, nome, email, cargo daquele usuário (não pode criar sem um cargo), cpf. Um usuário recém criado sempre vai estar como ativo."

## Clarifications

### Session 2026-11-04

- Q: Um usuário criado pode ficar sem cargo? → A: Não. Todo usuário criado precisa ter pelo menos um cargo vinculado.
- Q: Quem pode criar ou atribuir cargo a um usuário? → A: Somente o usuário com cargo Administrativo.

### Session 2026-11-15

- Q: Como o CPF deve ser gravado? → A: A coluna `usuario.cpf` passa a ser `VARCHAR(11)`; o código remove `.` e `-` e grava os 11 dígitos.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Administrativo cria um novo usuário (Priority: P1)

Um usuário com cargo Administrativo abre a área de administração, informa nome, e-mail, senha, cargo e CPF de uma nova pessoa e conclui o cadastro. O novo usuário passa a existir como ativo e consegue entrar no portal.

**Why this priority**: É a funcionalidade central da feature; sem ela os demais fluxos não existem.

**Independent Test**: Autenticar como Administrativo, cadastrar um usuário com cargo válido e confirmar que ele aparece na lista e consegue fazer login.

**Acceptance Scenarios**:

1. **Given** um Administrativo autenticado, **When** ele informa nome, e-mail, senha, pelo menos um cargo e CPF válidos, **Then** o usuário é criado com situação ativa.
2. **Given** um usuário recém-criado, **When** ele tenta entrar com o e-mail e a senha cadastrados, **Then** o login é aceito.
3. **Given** um usuário recém-criado, **When** o Administrativo consulta a lista de usuários, **Then** o novo usuário aparece com o cargo informado.

---

### User Story 2 - Validação dos dados de cadastro (Priority: P2)

Um Administrativo recebe mensagens claras quando tenta cadastrar um usuário com dados inválidos e o cadastro não é concluído.

**Why this priority**: Evita usuários incompletos ou duplicados e protege a consistência do acesso.

**Independent Test**: Tentar cadastrar sem cargo, sem nome, sem e-mail, sem senha, com e-mail já usado ou com CPF inválido e confirmar que cada caso é recusado com mensagem.

**Acceptance Scenarios**:

1. **Given** um Administrativo preenchendo o cadastro, **When** ele não seleciona um cargo, **Then** o cadastro é recusado com mensagem de cargo obrigatório.
2. **Given** um Administrativo, **When** ele informa um e-mail já cadastrado, **Then** o cadastro é recusado e nenhum usuário novo é criado.
3. **Given** um Administrativo, **When** ele deixa nome, e-mail ou senha em branco, **Then** o cadastro é recusado com mensagem de campo obrigatório.
4. **Given** um Administrativo, **When** ele informa um CPF que não tem 11 dígitos, **Then** o cadastro é recusado com mensagem de CPF inválido.

---

### User Story 3 - Restrição de quem pode cadastrar (Priority: P3)

Somente usuários com cargo Administrativo acessam a criação de usuários. Os demais cargos não veem a opção e não conseguem concluir o cadastro.

**Why this priority**: Garante o controle de acesso definido pela CPA.

**Independent Test**: Autenticar com Aluno, Coordenador e CPA Externo, conferir que a opção de cadastro não aparece e que uma tentativa direta é bloqueada.

**Acceptance Scenarios**:

1. **Given** um Coordenador autenticado, **When** ele acessa a área de administração, **Then** a opção de criar usuário não é exibida.
2. **Given** um Aluno autenticado, **When** ele tenta acessar a criação de usuário por endereço direto, **Then** o acesso é negado.

---

### Edge Cases

- O que acontece quando o Administrativo tenta criar um usuário com e-mail igual ao de outro usuário?
- O que acontece quando o CPF não é informado?
- O que acontece quando o CPF é informado com formatação (pontos e traço)?
- O que acontece quando a senha tem menos de 8 caracteres?
- O que acontece se o cadastro falhar no meio do processo?
- O que acontece quando o Administrativo tenta criar outro Administrativo?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST permitir que somente usuários com cargo Administrativo criem novos usuários.
- **FR-002**: O sistema MUST oferecer um formulário de cadastro com nome, e-mail, senha, cargo e CPF.
- **FR-003**: O sistema MUST exigir pelo menos um cargo vinculado no cadastro, não permitindo cadastro sem cargo.
- **FR-004**: O sistema MUST aceitar um ou mais dos cargos Aluno, Coordenador, Administrativo e CPA Externo.
- **FR-005**: O sistema MUST exigir nome, e-mail e senha no cadastro.
- **FR-006**: O sistema MUST aceitar CPF como campo opcional; quando informado, MUST ter 11 dígitos. O código MUST remover pontos e traço e MUST gravar apenas os dígitos na coluna `usuario.cpf` (`VARCHAR(11)`).
- **FR-007**: O sistema MUST impedir o cadastro quando o e-mail já estiver em uso, exibindo mensagem clara.
- **FR-008**: O sistema MUST exigir senha com no mínimo 8 caracteres.
- **FR-009**: O sistema MUST criar o novo usuário com situação ativa.
- **FR-010**: O sistema MUST exibir confirmação após o cadastro e incluir o novo usuário na lista.
- **FR-011**: O novo usuário MUST conseguir autenticar com o e-mail e a senha cadastrados.
- **FR-012**: O sistema MUST ocultar a opção de cadastro para perfis diferentes de Administrativo e MUST negar tentativas de acesso direto.
- **FR-013**: O sistema MUST atribuir ao novo usuário pelo menos um cargo selecionado no cadastro.

### Key Entities

- **Usuario**: pessoa que acessa o portal; possui nome, e-mail, senha, um ou mais cargos, CPF (opcional) e situação ativa.
- **Cargo**: nível de acesso do usuário; valores Aluno, Coordenador, Administrativo e CPA Externo.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Um Administrativo conclui o cadastro de um usuário em menos de 2 minutos.
- **SC-002**: 100% das tentativas de cadastro sem cargo são recusadas com mensagem clara.
- **SC-003**: 100% das tentativas com e-mail duplicado são recusadas.
- **SC-004**: 100% das tentativas de cadastro por perfis diferentes de Administrativo são bloqueadas.
- **SC-005**: 95% dos usuários recém-criados conseguem fazer login na primeira tentativa.

## Assumptions

- Os cargos disponíveis são os suportados pelo sistema atual: Aluno, Coordenador, Administrativo e CPA Externo.
- O CPF é opcional; quando informado, é tratado como identificador de 11 dígitos.
- A coluna `usuario.cpf` é `VARCHAR(11)` e recebe o CPF já normalizado, preservando zeros a esquerda.
- O e-mail é único por usuário.
- A senha é definida pelo Administrativo no momento do cadastro e deve ter no mínimo 8 caracteres.
- O usuário recém-criado fica sempre ativo.
- Somente o Administrativo cria usuários e atribui cargos; o Coordenador não participa deste fluxo nesta entrega.
- Todo usuário criado tem pelo menos um cargo vinculado; não é possível criar usuário sem cargo.
