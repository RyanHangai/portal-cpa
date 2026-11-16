# Feature Specification: Recuperação de Senha e Sessão Persistente

**Feature Branch**: `003-recuperacao-senha-sessao`

**Created**: 2026-11-15

**Status**: Draft

**Input**: User description: "agora qualquer tipo de usuario pode trocar a sua senha atual, para isso no campo de login vai aparecer uma opcao de recuperacai de senha, depois que ele clicar naquele campo, ele vai colocar o email desejado e depois uma senha e no final uma confirmacao dessa senha. Tambem vai adicionar o cookis de site para manter uma sessao de um usuario que ja logou, essa sessao vai se manter por 1 semana a partir de cada login feito. Isso vai fazer com que mesmo recarregando a pagina o usuario fique logado"

## Clarifications

### Session 2026-11-15

- Q: A troca de senha deve exigir alguma prova de identidade além do e-mail da conta? → A: Sim. A troca só é concluída após confirmação de um usuário com cargo Administrativo; o pedido fica pendente até a decisão.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Solicitar a troca de senha e concluí-la com aprovação administrativa (Priority: P1)

Qualquer usuário, de qualquer cargo, que não consegue entrar no portal abre a tela de login, aciona a opção de recuperação de senha, informa o e-mail da conta, define uma nova senha e repete a senha no campo de confirmação. O pedido fica pendente e um usuário com cargo Administrativo confirma a troca; só então a nova senha passa a valer.

**Why this priority**: é o valor central da feature; sem isso o usuário que esqueceu a senha continua dependendo de outra pessoa para recuperar o acesso.

**Independent Test**: em um usuário de teste, abrir a tela de login, acionar a recuperação, enviar e-mail, nova senha e confirmação; em seguida aprovar o pedido como Administrativo e confirmar que o login seguinte só é aceito com a senha nova.

**Acceptance Scenarios**:

1. **Given** um visitante na tela de login, **When** ele aciona a opção de recuperação de senha, **Then** o sistema exibe os campos de e-mail, nova senha e confirmação da nova senha.
2. **Given** o formulário de recuperação preenchido com e-mail de conta ativa, nova senha com pelo menos 8 caracteres e confirmação idêntica, **When** ele envia o formulário, **Then** o pedido fica pendente, uma mensagem neutra é exibida e a senha atual continua valendo.
3. **Given** um pedido pendente, **When** um Administrativo o visualiza e aprova, **Then** a senha do solicitante passa a ser a nova senha informada no pedido.
4. **Given** um pedido aprovado, **When** o usuário tenta entrar com e-mail e senha nova, **Then** o acesso é aceito.
5. **Given** um pedido aprovado, **When** o usuário tenta entrar com a senha antiga, **Then** o acesso é negado.
6. **Given** um pedido pendente, **When** um Administrativo o recusa, **Then** a senha permanece inalterada, o pedido é descartado e a senha nova é negada no login.
7. **Given** um pedido pendente do usuário, **When** ele envia um novo pedido, **Then** o pedido anterior é substituído pelo novo.
8. **Given** um pedido pendente há mais de 24 horas, **When** um Administrativo consulta a lista, **Then** o pedido não aparece mais e a senha permanece inalterada.
9. **Given** um usuário com cargo diferente de Administrativo, **When** ele tenta consultar os pedidos pendentes, **Then** a lista e as ações de aprovar ou recusar não são exibidas.

---

### User Story 2 - Permanecer logado por uma semana (Priority: P2)

Depois de entrar no portal, o usuário continua autenticado ao recarregar a página, fechar a aba ou reabrir o navegador, até uma semana depois daquele login. Passado o prazo, ou ao sair, o acesso volta a exigir login.

**Why this priority**: evita que o usuário digite a senha a cada recarga e é o outro comportamento pedido, mas depende do login já existente para ser percebido.

**Independent Test**: entrar no portal, recarregar a página e reabrir o navegador, confirmando que o usuário continua autenticado; depois simular o fim do prazo e confirmar que o login volta a ser exigido.

**Acceptance Scenarios**:

1. **Given** um usuário autenticado, **When** ele recarrega a página ou reabre o navegador dentro do prazo de uma semana, **Then** ele permanece autenticado, sem digitar a senha novamente.
2. **Given** um usuário autenticado há mais de uma semana, **When** ele volta ao portal, **Then** a sessão é encerrada e o login é exigido.
3. **Given** um usuário autenticado, **When** ele aciona "Sair", **Then** a sessão é encerrada e o acesso volta a exigir login.
4. **Given** um usuário que entrou novamente no portal, **When** o novo login é concluído, **Then** o prazo de uma semana passa a ser contado a partir desse novo login.

---

### User Story 3 - Recusar recuperações inválidas com mensagens claras (Priority: P3)

Quem tenta recuperar a senha com dados incompletos, senha curta, confirmação divergente ou e-mail sem conta recebe uma recusa clara, e a senha não é alterada.

**Why this priority**: protege a integridade do acesso e evita que erros de digitação troquem a senha errada, mas só importa depois que o fluxo principal existe.

**Independent Test**: enviar o formulário de recuperação com cada tipo de dado inválido e confirmar que cada caso é recusado com mensagem própria e que a senha antiga continua funcionando.

**Acceptance Scenarios**:

1. **Given** o formulário de recuperação, **When** o e-mail, a nova senha ou a confirmação estão em branco, **Then** a troca é recusada com mensagem de campo obrigatório.
2. **Given** o formulário de recuperação, **When** a nova senha tem menos de 8 caracteres, **Then** a troca é recusada com mensagem de senha mínima.
3. **Given** o formulário de recuperação, **When** a confirmação não coincide com a nova senha, **Then** a troca é recusada com mensagem de confirmação divergente.
4. **Given** o formulário de recuperação, **When** o e-mail não pertence a nenhuma conta ativa, **Then** o pedido é recusado com a mesma mensagem neutra dos pedidos válidos e nenhuma senha é alterada.

---

### Edge Cases

- O que acontece quando o e-mail informado não existe ou pertence a um usuário inativo?
- O que acontece quando o e-mail é digitado com letras maiúsculas ou espaços nas pontas?
- O que acontece quando a nova senha é igual à senha atual?
- O que acontece quando o pedido fica pendente e nenhum Administrativo decide dentro de 24 horas?
- O que acontece quando o usuário é desativado enquanto tem um pedido pendente?
- O que acontece quando dois Administrativos decidem o mesmo pedido quase ao mesmo tempo?
- O que acontece quando a sessão expira enquanto o usuário navega?
- O que acontece quando o usuário é desativado enquanto possui uma sessão válida?
- O que acontece quando a informação de sessão guardada no navegador é adulterada ou removida?
- O que acontece quando o usuário sai em um navegador, mas está autenticado em outro?
- O que acontece quando a senha é trocada enquanto existe sessão ativa em outro dispositivo?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST oferecer, na tela de login, uma opção de recuperação de senha acessível a qualquer usuário, independentemente do cargo.
- **FR-002**: O fluxo de recuperação MUST solicitar o e-mail da conta, a nova senha e a confirmação da nova senha, e MUST registrar o pedido como pendente até a decisão de um Administrativo.
- **FR-003**: O sistema MUST exigir nova senha com no mínimo 8 caracteres, mantendo a regra já vigente no portal.
- **FR-004**: O sistema MUST recusar a troca quando a confirmação não coincidir com a nova senha, exibindo mensagem específica.
- **FR-005**: O sistema MUST recusar o pedido quando o e-mail não corresponder a uma conta ativa, sem registrar pedido e sem alterar nenhum dado, exibindo a mesma mensagem neutra usada nos pedidos válidos, de modo que não seja possível descobrir se o e-mail está cadastrado.
- **FR-006**: O sistema MUST atualizar apenas a senha do usuário; nome, e-mail, cargos, CPF e situação ativa MUST permanecer inalterados.
- **FR-007**: O sistema MUST comparar o e-mail informado ignorando diferenças entre maiúsculas e minúsculas e espaços nas pontas.
- **FR-008**: Após a aprovação do pedido, o sistema MUST aplicar a nova senha, que passa a ser exigida no login seguinte.
- **FR-009**: O sistema MUST NOT exibir a senha em nenhuma tela após a gravação.
- **FR-010**: O sistema MUST manter a sessão do usuário autenticado por 168 horas (uma semana) contadas a partir do login bem-sucedido, de forma absoluta, sem renovação por atividade.
- **FR-011**: Enquanto a sessão estiver válida, o sistema MUST manter o usuário autenticado após recarregar a página, fechar e reabrir a aba ou reabrir o navegador.
- **FR-012**: Cada novo login MUST reiniciar a contagem de 168 horas da sessão.
- **FR-013**: Ao atingir o prazo de 168 horas, o sistema MUST encerrar a sessão e exigir novo login.
- **FR-014**: A ação "Sair" MUST encerrar a sessão persistida, removendo a informação de sessão guardada no navegador.
- **FR-015**: A sessão persistida MUST NOT conter a senha nem permitir recuperá-la; uma sessão adulterada, inválida ou expirada MUST ser tratada como não autenticada.
- **FR-016**: Quando o usuário estiver inativo, a sessão persistida MUST ser considerada inválida no acesso seguinte.
- **FR-017**: O sistema MUST permitir que usuários com cargo Administrativo vejam os pedidos pendentes, com o e-mail do solicitante e o momento do pedido, e aprovem ou recusem cada um.
- **FR-018**: A senha MUST ser alterada somente depois da aprovação; na recusa, a senha MUST permanecer inalterada e o pedido MUST ser descartado.
- **FR-019**: O Administrativo MUST NOT ver a nova senha solicitada; o pedido MUST reter essa senha apenas para aplicá-la na aprovação.
- **FR-020**: Um novo pedido do mesmo usuário MUST substituir o pedido pendente anterior.
- **FR-021**: Pedido sem decisão em 24 horas MUST expirar e MUST NOT alterar a senha.
- **FR-022**: Somente usuários com cargo Administrativo MUST poder listar, aprovar ou recusar pedidos de troca de senha.
- **FR-023**: Quando dois Administrativos decidirem o mesmo pedido, a primeira decisão MUST valer e a segunda MUST ser ignorada.

### Key Entities *(include if feature involves data)*

- **Usuário**: pessoa que acessa o portal; possui nome, e-mail, senha, um ou mais cargos, CPF e situação ativa. A recuperação altera somente a senha.
- **Solicitação de troca de senha**: pedido feito na tela de login; possui o solicitante, a nova senha pretendida, o momento do pedido, a situação (pendente, aprovada, recusada ou expirada) e, quando decidida, o Administrativo responsável pela decisão.
- **Sessão autenticada**: vínculo entre um usuário e um navegador, criado a cada login bem-sucedido; possui o usuário associado, o momento do login e o momento de expiração, 168 horas depois.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% dos usuários autenticados continuam autenticados ao recarregar a página ou reabrir o navegador dentro das 168 horas seguintes ao login.
- **SC-002**: 100% das sessões deixam de valer após 168 horas contadas do login, exigindo novo acesso.
- **SC-003**: Um usuário conclui a solicitação de troca em menos de 1 minuto e um Administrativo decide o pedido em menos de 2 minutos.
- **SC-004**: 100% das tentativas com confirmação divergente, senha com menos de 8 caracteres, campo em branco ou e-mail sem conta ativa são recusadas, sem registrar pedido e sem alterar a senha.
- **SC-005**: Nenhuma mensagem do fluxo de recuperação revela se um e-mail está ou não cadastrado.
- **SC-006**: Nenhuma senha é exibida em tela, nem para o solicitante nem para o Administrativo, durante a análise ou após a gravação.
- **SC-007**: 100% das senhas são alteradas somente depois de uma aprovação; recusas e expirações não alteram a senha em nenhum caso.

## Assumptions

- A sessão é mantida no navegador do usuário; os pedidos de troca de senha precisam ser guardados no servidor para que qualquer Administrativo os veja, e a forma de armazenamento é decidida no planejamento.
- "Uma semana" equivale a 168 horas contadas de forma absoluta a partir de cada login, sem renovação por atividade, alinhado ao comportamento já descrito na especificação do portal.
- Cada login gera uma sessão independente por navegador; sair em um navegador não encerra sessões abertas em outros.
- A troca de senha não invalida sessões já abertas em outros navegadores; elas seguem até o prazo natural.
- O fluxo não depende de envio de e-mail, código ou link; a confirmação é feita por um usuário com cargo Administrativo.
- Pedidos pendentes expiram em 24 horas e não são aprovados automaticamente.
- O Administrativo pode recusar um pedido sem informar motivo nesta entrega.
- A nova senha pode ser igual à senha atual; não há bloqueio de reutilização nesta entrega.
- A recuperação mediada por um usuário administrativo, já existente no portal, continua disponível como alternativa.
- O portal continua com o formato atual de armazenamento de senha; o armazenamento seguro de senhas segue registrado como pendência de segurança.
- Não há limite de tentativas para a recuperação nesta entrega; o controle de abuso fica registrado como pendência.
- Usuários inativos não conseguem solicitar troca, têm pedidos descartados e perdem a sessão persistida.
- O e-mail é identificado sem diferenciar maiúsculas, minúsculas e espaços nas pontas, como já ocorre no cadastro.
