# Feature Specification: Portal de Transparência da CPA

**Feature Branch**: `001-portal-cpa`

**Created**: 2026-11-04

**Status**: Draft

**Input**: User description: "Desenvolver um portal web para a CPA que centralize e apresente, de forma estruturada e com controle de acesso, os dashboards das pesquisas institucionais, as devolutivas das áreas e os relatórios, possibilitando que alunos, coordenadores, avaliadores externos e a comunidade em geral acessem as informações pertinentes ao seu perfil"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Acesso autenticado com direcionamento por perfil (Priority: P1)

Um integrante da comunidade (aluno, professor, coordenador, diretor, administrativo ou avaliador externo) informa suas credenciais e passa a ver apenas o conteúdo permitido ao seu perfil.

**Why this priority**: Sem autenticação e controle de acesso não é possível garantir que cada público veja somente as informações pertinentes; é a base de todos os demais fluxos.

**Independent Test**: Pode ser testado criando um usuário de cada perfil, autenticando e verificando que o portal direciona para a página inicial correta e bloqueia páginas não permitidas.

**Acceptance Scenarios**:

1. **Given** um usuário com credenciais válidas, **When** ele faz login, **Then** é direcionado à página inicial compatível com o seu perfil.
2. **Given** um visitante sem login, **When** tenta abrir uma página restrita, **Then** o portal solicita autenticação e não exibe o conteúdo.
3. **Given** um usuário autenticado há mais de 168 horas, **When** tenta navegar novamente, **Then** a sessão é encerrada e o login é exigido.
4. **Given** credenciais inválidas, **When** o usuário tenta entrar, **Then** o portal exibe mensagem de erro e não concede acesso.

---

### User Story 2 - Dashboards personalizados por perfil (Priority: P2)

Um usuário autenticado visualiza, na página inicial, apenas os dashboards de pesquisas institucionais permitidos ao seu perfil.

**Why this priority**: É o núcleo do propósito do portal: dar transparência estruturada aos resultados das pesquisas para cada público.

**Independent Test**: Pode ser testado autenticando com cada perfil e conferindo quais dashboards aparecem e se os não permitidos ficam ocultos e inacessíveis.

**Acceptance Scenarios**:

1. **Given** um aluno autenticado, **When** acessa a página inicial, **Then** vê apenas os dashboards permitidos ao perfil aluno.
2. **Given** um coordenador autenticado, **When** acessa a página inicial, **Then** vê os dashboards institucionais permitidos ao perfil coordenador.
3. **Given** um avaliador externo autenticado, **When** acessa a página inicial, **Then** vê todos os dashboards institucionais.
4. **Given** um perfil sem permissão para um dashboard, **When** tenta acessá-lo por endereço direto, **Then** o acesso é negado.

---

### User Story 3 - Mural de devolutivas público (Priority: P3)

Qualquer pessoa da comunidade acessa um mural público com as resoluções e respostas das áreas às demandas das pesquisas, sem necessidade de login.

**Why this priority**: É o principal instrumento de prestação de contas pública e não depende de autenticação.

**Independent Test**: Pode ser testado acessando o mural sem login e verificando que as devolutivas publicadas ficam visíveis.

**Acceptance Scenarios**:

1. **Given** um visitante sem login, **When** abre o mural de devolutivas, **Then** visualiza as devolutivas publicadas.
2. **Given** uma devolutiva publicada, **When** o visitante a abre, **Then** vê o conteúdo completo (área, demanda, resposta e data).

---

### User Story 4 - Área de relatórios e boletins (Priority: P4)

Um usuário autenticado consulta e baixa documentos institucionais, como relatórios de autoavaliação e boletins informativos, conforme o seu perfil.

**Why this priority**: Concentra em um único lugar a documentação institucional que hoje está dispersa.

**Independent Test**: Pode ser testado autenticando com perfis diferentes e verificando a lista de documentos visível e o download.

**Acceptance Scenarios**:

1. **Given** um usuário autenticado com permissão, **When** abre a área de relatórios, **Then** vê a lista de documentos permitidos e consegue abri-los.
2. **Given** um perfil sem permissão para um documento, **When** tenta acessá-lo, **Then** o acesso é negado.

---

### User Story 5 - Página de contato (Priority: P5)

Qualquer visitante acessa uma página de contato com atalhos para os canais oficiais da CPA.

**Why this priority**: Facilita a comunicação da comunidade com a CPA, com baixo custo de implementação.

**Independent Test**: Pode ser testado acessando a página sem login e conferindo que os atalhos levam aos canais corretos.

**Acceptance Scenarios**:

1. **Given** um visitante sem login, **When** abre a página de contato, **Then** vê os atalhos de comunicação da CPA.
2. **Given** um atalho exibido, **When** o visitante o seleciona, **Then** é redirecionado ao canal correspondente.

---

### Edge Cases

- O que acontece quando o usuário tenta acessar uma página restrita sem estar autenticado?
- Como o sistema trata um usuário que possui mais de um perfil?
- O que acontece quando um dashboard externo está indisponível?
- Como o sistema trata a recuperação de senha quando não há autoatendimento?
- O que acontece quando um documento é removido ou substituído?
- Como o sistema se comporta quando a sessão expira durante a navegação?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST permitir autenticação de usuários com credenciais válidas.
- **FR-002**: O sistema MUST direcionar o usuário autenticado para a página inicial compatível com o seu perfil.
- **FR-003**: O sistema MUST suportar os perfis Aluno, Professor, Coordenador, Diretor, Administrativo e CPA Externo.
- **FR-004**: O sistema MUST exibir dashboards de pesquisas institucionais conforme as permissões do perfil do usuário.
- **FR-005**: O sistema MUST garantir que dashboards e relatórios não permitidos ao perfil não sejam exibidos na navegação nem acessíveis por qualquer rota, inclusive por acesso direto.
- **FR-006**: O sistema MUST permitir acesso à base de dados bruta apenas aos perfis Diretor e Administrativo. "Base de dados bruta" designa a visualização e a exportação, em formato tabular e somente leitura, dos registros das entidades de domínio (usuários e perfis), oferecidas por uma tela autenticada, sem exposição de credenciais nem acesso direto ao SGBD.
- **FR-007**: O sistema MUST publicar um mural de devolutivas acessível sem autenticação.
- **FR-008**: O sistema MUST disponibilizar uma área de relatórios e boletins com documentos institucionais.
- **FR-009**: O sistema MUST disponibilizar uma página de contato com atalhos para os canais oficiais da CPA.
- **FR-010**: O sistema MUST encerrar a sessão do usuário 168 horas após o último login bem-sucedido, contadas de forma absoluta (não deslizante por atividade).
- **FR-011**: O sistema MUST permitir que os perfis Administrativo, Diretor e Coordenador criem e gerenciem usuários, sendo o Coordenador restrito aos usuários vinculados ao próprio curso.
- **FR-012**: O sistema MUST restringir a gestão de cursos ao Coordenador (do próprio curso), Administrativo e Diretor.
- **FR-013**: O sistema MUST registrar eventos de acesso a conteúdo restrito para fins de auditoria, armazenando usuário, recurso, ação, resultado (permitido ou negado) e data e hora. Os registros MUST ser mantidos por no mínimo 12 meses.
- **FR-014**: O sistema MUST permitir recuperação de senha mediada por um usuário de nível superior.

### Key Entities *(include if feature involves data)*

- **Usuário**: pessoa que acessa o portal; possui nome, e-mail, senha, situação ativa e data de nascimento, e pode ter um ou mais perfis.
- **Perfil**: nível de acesso (Aluno, Professor, Coordenador, Diretor, Administrativo, CPA Externo) que define as permissões.
- **Aluno**: usuário com vínculo a um curso.
- **Curso**: oferta acadêmica à qual alunos e coordenadores se vinculam.
- **Dashboard**: painel de resultados de pesquisa institucional associado a perfis permitidos.
- **Devolutiva**: resposta ou resolução de uma área às demandas das pesquisas, com área responsável, descrição e data.
- **Relatório/Boletim**: documento institucional armazenado e consultável, com categoria e visibilidade.
- **Canal de Contato**: atalho para comunicação oficial da CPA.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Um usuário autenticado encontra o dashboard do seu perfil em menos de 1 minuto a partir do login.
- **SC-002**: 100% das tentativas de acesso a conteúdo restrito por perfis não autorizados são bloqueadas.
- **SC-003**: 95% dos usuários concluem o login na primeira tentativa.
- **SC-004**: O mural de devolutivas é acessível sem autenticação em 100% das tentativas.
- **SC-005**: A quantidade de solicitações manuais de relatórios e dashboards cai pelo menos 50% em até 6 meses após a adoção, medida pela contagem de pedidos registrados pela CPA.
- **SC-006**: 90% dos avaliadores externos localizam todos os relatórios institucionais na primeira sessão.

## Assumptions

- A comunidade em geral acessa sem login apenas as páginas públicas (mural de devolutivas e contato); dashboards e relatórios exigem autenticação.
- A autenticação é feita com e-mail e senha, com recuperação de senha mediada por um usuário de nível superior, conforme as regras vigentes da CPA.
- Os dashboards das pesquisas já existem e são mantidos pela instituição; o portal apenas os incorpora, sem recriá-los.
- A sessão permanece válida por 168 horas (uma semana) após o login.
- O escopo inicial concentra-se em apresentar e controlar o acesso ao conteúdo; a edição e publicação de conteúdo institucional pode evoluir em entregas seguintes.
- Os dados de usuários, cursos, permissões e documentos são mantidos em base persistente.
- O acesso à base bruta é feito por uma tela autenticada e somente leitura, com exportação tabular; não há conexão direta ao banco por usuários do portal.
- A gestão de aulas, disciplinas e turmas não faz parte do escopo inicial; apenas cursos são geridos nesta entrega.
- A base de dados bruta é acessível a Diretor e Administrativo (FR-006). O RNF04 de `levantamento_requisitos/requisitos.md` diverge ao excluir o Diretor; prevalece FR-006, e a divergência deve ser confirmada com a CPA antes da implementação.
- A senha deve ter no mínimo 8 caracteres; após 5 tentativas de login inválidas consecutivas, a conta é bloqueada temporariamente por 15 minutos.
