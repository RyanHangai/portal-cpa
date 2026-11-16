# Data Model: Cadastro de Usuário pelo Administrativo

> Baseado no schema atual de `database/database.sql` (DrawDB) e na spec 002.

## Entrada do cadastro

### DadosCadastroUsuario
| Campo | Tipo | Regras |
|-------|------|--------|
| nome | texto | Obrigatorio |
| email | texto | Obrigatorio; unico na aplicacao; normalizado para minusculo e sem espacos nas pontas |
| senha | texto | Obrigatorio; minimo de 8 caracteres |
| cargos | lista de cargo | Pelo menos um; valores permitidos Aluno, Coordenador, Administrativo e CPA Externo |
| curso | curso (enum) | Obrigatorio somente quando Aluno estiver entre os cargos |
| cpf | texto de 11 digitos | Opcional; quando informado, exatamente 11 digitos numericos; o codigo remove `.` e `-` e grava apenas os digitos |

### cargo (enum)
Valores: `aluno`, `coordenador`, `administrativo`, `cpa_externo`.

### curso (enum)
Valores: `ciencia da computacao`, `engenharia de software`, `analise de sistemas`,
`sistema da informacao`.

## Entidades persistidas

### usuario
| Campo | Regras no cadastro |
|-------|--------------------|
| id | Gerado automaticamente |
| nome | Obrigatorio |
| email | Obrigatorio; verificado como unico na aplicacao |
| senha | Obrigatorio; minimo de 8 caracteres |
| ativo | Sempre TRUE no cadastro |
| data_nasc | Nao informado nesta feature |
| cpf | Opcional; coluna `VARCHAR(11)`; gravado apenas com os 11 digitos |
| aluno_id | Preenchido somente se Aluno estiver entre os cargos |
| coordenador_id | Preenchido somente se Coordenador estiver entre os cargos |
| admin_id | Preenchido somente se Administrativo estiver entre os cargos |
| cpa_externo_id | Preenchido somente se CPA Externo estiver entre os cargos |

### aluno
| Campo | Regras |
|-------|--------|
| id | Igual ao `usuario.id` |
| curso | Obrigatorio |

### coordenador
| Campo | Regras |
|-------|--------|
| id | Igual ao `usuario.id` |

### administrativo
| Campo | Regras |
|-------|--------|
| id | Igual ao `usuario.id` |

### cpa_externo
| Campo | Regras |
|-------|--------|
| id | Igual ao `usuario.id` |

## Regras de validacao
- Nome, e-mail e senha obrigatorios.
- Senha com no minimo 8 caracteres.
- Pelo menos um cargo selecionado.
- Cargo Aluno exige curso.
- CPF opcional; quando informado, 11 digitos numericos.
- CPF e normalizado removendo `.` e `-` e gravado como texto de 11 digitos na coluna `VARCHAR(11)`.
- E-mail unico na aplicacao.
- Novo usuario sempre ativo.

## Fluxo de criacao (transacao unica)
1. Validar os dados de entrada.
2. Verificar se o e-mail ja existe; se existir, abortar com erro de e-mail duplicado.
3. Inserir `usuario` com `ativo = TRUE` e obter `usuario_id`.
4. Para cada cargo selecionado, executar os passos da secao R2 de `research.md`,
   usando `usuario_id` como id do perfil.
5. Confirmar a transacao e retornar o usuario criado.

> A unica alteracao de schema desta feature e o tipo de `usuario.cpf`, que passa de
> `INTEGER` para `VARCHAR(11)` em `database/database.sql`.
