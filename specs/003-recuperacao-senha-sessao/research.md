# Research: Recuperação de Senha e Sessão Persistente

## Decisoes

### R1. Onde guardar as solicitacoes de troca de senha
- Decision: criar a tabela `solicitacao_senha` em `database/database.sql`, com o tipo
  enumerado `situacao_solicitacao` (`pendente`, `aprovada`, `recusada`, `expirada`).
- Rationale: o pedido precisa sobreviver entre requisicoes e sessoes para que qualquer
  Administrativo o veja e decida. O schema atual nao tem onde guardar esse estado.
- Alternatives considered: colunas extras em `usuario` (poluiria a tabela de identidade e
  permitiria apenas um pedido, sem historico de decisao); guardar no cookie (nenhum
  Administrativo veria o pedido de outra pessoa).
- Consequence: existe uma alteracao de schema nesta feature. Bancos ja criados precisam de
  volume novo (`docker compose down -v`), porque `database.sql` so roda na primeira
  criacao do volume.

### R2. Leitura e escrita do cookie de sessao
- Decision: ler o cookie de `st.context.cookies`, que vem do cabecalho da requisicao, e
  gravar ou remover com um script de uma linha em `st.components.v1.html`, sempre com
  `path=/`, `max-age` de 168 horas e `SameSite=Lax`.
- Rationale: a leitura sincrona permite restaurar a sessao antes de montar a navegacao, e
  a escrita com atributos explicitos nao depende do formato interno de um componente de
  terceiros.
- Alternatives considered: `extra-streamlit-components` (usado primeiro, mas o cookie nao
  era restaurado ao recarregar e o componente ainda gerava `CachedWidgetWarning`);
  `streamlit-cookies-controller` (sem manutencao).
- Note: a gravacao e a remocao sao aplicadas na execucao seguinte ao login ou ao logout,
  porque um `st.rerun` imediato descarta o elemento que executa o script no navegador.

### R3. Formato e assinatura do token de sessao
- Decision: token no formato `<payload_base64url>.<assinatura_base64url>`, com payload JSON
  contendo `usuario_id` e `login_em` (data e hora em UTC) e assinatura HMAC-SHA256 usando
  `cookie_secret()` de `src/config.py`.
- Rationale: impede adulteracao sem exigir dependencia de criptografia e sem guardar a
  senha. A comparacao da assinatura usa `hmac.compare_digest`.
- Alternatives considered: JWT (dependencia nova para o mesmo efeito); guardar apenas o
  id do usuario (permitiria falsificar a sessao trocando o valor do cookie).
- Note: `COOKIE_SECRET` tem valor padrao de desenvolvimento em `src/config.py`; em
  producao deve vir de variavel de ambiente.

### R4. Duracao e revalidacao da sessao
- Decision: a expiracao e absoluta, 168 horas contadas de `login_em`; nao existe renovacao
  por atividade. A cada carga de pagina o token e validado e o usuario e buscado no banco
  para conferir se continua ativo.
- Rationale: atende FR-010 a FR-016 e a regra ja descrita na especificacao do portal.
- Alternatives considered: expiracao deslizante (contraria a especificacao); confiar apenas
  no prazo do cookie (um cookie copiado continuaria valido indefinidamente).
- Note: o cookie e gravado com `expires` de 168 horas e `path=/`; o prazo do cookie e do
  token precisam coincidir.

### R5. Expiracao das solicitacoes pendentes
- Decision: antes de listar, marcar como `expirada` toda solicitacao `pendente` com
  `criado_em` anterior a `NOW() - INTERVAL '24 hours'`, na mesma transacao da listagem.
- Rationale: evita um processo agendado e mantem a lista sempre consistente para o
  Administrativo.
- Alternatives considered: tarefa periodica (complexidade desnecessaria); ignorar pedidos
  antigos apenas na leitura (deixaria registros `pendente` sem sentido).

### R6. Um pedido pendente por usuario
- Decision: ao registrar um pedido, apagar o pedido `pendente` anterior do mesmo usuario e
  inserir o novo, na mesma transacao.
- Rationale: atende FR-020 sem exigir indice parcial no banco e mantem a lista simples.
- Alternatives considered: indice unico parcial em `solicitacao_senha (usuario_id)` com
  `situacao = 'pendente'` (mais robusto contra concorrencia, mas mais um objeto de schema
  para um cenario raro); acumular varios pedidos (confundiria o Administrativo).

### R7. Mensagem neutra no envio do pedido
- Decision: exibir a mesma mensagem para e-mail existente e inexistente, por exemplo
  "Se os dados estiverem corretos, o pedido sera analisado por um Administrativo.".
- Rationale: atende FR-005 e SC-005, impedindo descobrir quais e-mails estao cadastrados.
- Alternatives considered: mensagem especifica de "usuario nao encontrado" (revelaria a
  existencia da conta).

### R8. Decisao idempotente
- Decision: aprovar e recusar atualizam somente linhas com `situacao = 'pendente'`; quando
  nenhuma linha e afetada, a decisao e ignorada sem erro e a tela recarrega a lista.
- Rationale: atende FR-023 para duas decisoes simultaneas.
- Alternatives considered: levantar erro de conflito (ruido para o Administrativo, sem
  ganho pratico).

### R9. Onde ficam as telas
- Decision: o formulario de recuperacao fica na barra lateral de login em `src/main.py`,
  dentro de um expansor; a lista de solicitacoes pendentes fica em
  `src/views/administracao.py`, visivel apenas para Administrativo.
- Rationale: reaproveita os pontos de entrada existentes e o mesmo controle de acesso ja
  usado no cadastro de usuarios.
- Alternatives considered: uma pagina propria de recuperacao (mais um item de navegacao
  para um fluxo esporadico).

## Unknowns residuais

Nenhuma pendencia bloqueante. A unica alteracao de schema esta descrita em R1 e depende de
recriar o volume do banco.
