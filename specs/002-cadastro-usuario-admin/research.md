# Research: Cadastro de Usuário pelo Administrativo

## Decisoes

### R1. Gravacao atomica com vinculo de cargos
- Decision: criar o `usuario` e, na mesma transacao, vincular cada cargo usando o
  proprio `usuario.id` como id da tabela de perfil.
- Rationale: o schema usa FKs circulares. Para `aluno`, `coordenador` e
  `administrativo`, a FK fica na tabela de perfil apontando para `usuario.<cargo>_id`,
  entao o id do perfil precisa ser conhecido antes. Reutilizar o `usuario.id` evita
  sequencias e concorrencia no calculo de ids.
- Alternatives considered: usar `MAX(id) + 1` (sujeito a corrida) ou criar sequencias
  novas no banco (mudanca de schema desnecessaria).

### R2. Ordem de insercao por cargo
- Decision:
  - Administrativo: `UPDATE usuario SET admin_id = :id`; depois
    `INSERT INTO administrativo (id) VALUES (:id)`.
  - Coordenador: `UPDATE usuario SET coordenador_id = :id`; depois
    `INSERT INTO coordenador (id) VALUES (:id)`.
  - Aluno: `UPDATE usuario SET aluno_id = :id`; depois
    `INSERT INTO aluno (id, curso) VALUES (:id, :curso)`.
  - CPA Externo: `INSERT INTO cpa_externo (id) VALUES (:id)`; depois
    `UPDATE usuario SET cpa_externo_id = :id`.
- Rationale: respeita a direcao de cada chave estrangeira do schema atual.
- Alternatives considered: inserir o perfil antes do `usuario` (falha nas FKs em
  `aluno`, `coordenador` e `administrativo`).

### R3. Curso obrigatorio para o cargo Aluno
- Decision: quando o cargo Aluno for selecionado, o formulario exige um curso.
- Rationale: `aluno.curso` e NOT NULL no schema; sem curso o cadastro nao pode ser
  concluido.
- Alternatives considered: criar aluno sem curso (invalido) ou assumir um curso padrao
  (dado incorreto).
- Note: esta decisao precisa ser confirmada com o usuario; o texto original da feature
  nao citava curso.

### R4. Armazenamento do CPF
- Decision: alterar `usuario.cpf` para VARCHAR(11) em `database/database.sql` e gravar
  apenas os digitos, removendo `.`, `-` e qualquer caractere nao numerico.
- Rationale: o CPF tem 11 digitos e pode ter zeros a esquerda; VARCHAR(11) comporta o
  valor completo sem perda. O usuario autorizou explicitamente a troca do tipo.
- Alternatives considered: manter INTEGER (limite de 2.147.483.647, nao comporta 11
  digitos); BIGINT (comporta o valor, mas perde zeros a esquerda).
- Consequence: `database/database.sql` e a unica fonte do schema. Bancos criados antes
  desta alteracao precisam ser recriados com `docker compose down -v` e
  `docker compose up -d --build`.

### R5. Unicidade de e-mail
- Decision: verificar na aplicacao, dentro da transacao, se o e-mail ja existe antes
  de inserir; se existir, recusar o cadastro.
- Rationale: `usuario.email` nao tem constraint UNIQUE no schema atual.
- Alternatives considered: criar indice UNIQUE no banco (mudanca de schema).
- Note: a checagem na aplicacao reduz o risco, mas nao elimina concorrencia; um indice
  UNIQUE no futuro seria a garantia definitiva.

### R6. Politica de senha
- Decision: exigir no minimo 8 caracteres e gravar na coluna `senha` como o sistema ja
  faz hoje.
- Rationale: mantem compatibilidade com o login atual.
- Note: a senha continua em texto puro por causa do schema; migrar para hash e uma
  pendencia de seguranca registrada.

### R7. Multiplos cargos
- Decision: permitir selecionar um ou mais cargos; pelo menos um e obrigatorio.
- Rationale: o usuario reforcou "pelo menos um cargo" e o schema permite varios
  vinculos por usuario.
- Alternatives considered: exigir exatamente um cargo (mais simples, mas limitaria o
  cadastro).

### R8. Controle de acesso
- Decision: exibir o cadastro apenas para Administrativo e aplicar a mesma guarda na
  view.
- Rationale: atende FR-001 e FR-012 e mantem a defesa em profundidade.

## Unknowns residuais

- Tipo da coluna `cpf` (R4): resolvido; a coluna passa a ser VARCHAR(11) e recebe os
  11 digitos normalizados.
- Campo `curso` para Aluno (R3): assumido como obrigatorio quando Aluno for
  selecionado; confirmar com o usuario.

Nenhuma outra pendencia bloqueante.
