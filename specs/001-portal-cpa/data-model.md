# Data Model: Portal de Transparência da CPA

> Fontes iniciais: `database/database.sql` e `database/schema.json`. O schema atual
> é parcial e tem relações circulares; este documento define o modelo-alvo que a
> implementação deve materializar.

## Entidades

### usuario
| Campo | Tipo | Regras |
|-------|------|--------|
| id | integer, identity | Chave primária |
| nome | varchar(255) | Obrigatório |
| email | varchar(255) | Obrigatório, único, usado no login |
| senha_hash | varchar | Obrigatório, hash bcrypt, nunca texto puro |
| ativo | boolean | Obrigatório; inativo não autentica |
| data_nasc | date | Opcional |
| cpf | varchar(11) | Opcional, único quando informado |
| criado_em | timestamptz | Padrão `now()` |

Relações: 1:N com `usuario_perfil`; 1:0..1 com `aluno`, `professor`,
`coordenador`, `diretor`, `administrativo` e `cpa_externo`.

### perfil (enum)
Valores: `aluno`, `professor`, `coordenador`, `diretor`, `administrativo`,
`cpa_externo`.

### usuario_perfil
| Campo | Tipo | Regras |
|-------|------|--------|
| usuario_id | integer | FK `usuario`, parte da PK |
| perfil | perfil (enum) | Parte da PK |

### curso (enum)
Valores: `ciencia da computacao`, `engenharia de software`, `analise de sistemas`,
`sistema da informacao`.

### aluno
| Campo | Tipo | Regras |
|-------|------|--------|
| usuario_id | integer | PK e FK `usuario` |
| ra | varchar(20) | Único, obrigatório |
| curso | curso (enum) | Obrigatório |

### professor
| Campo | Tipo | Regras |
|-------|------|--------|
| usuario_id | integer | PK e FK `usuario` |

### coordenador
| Campo | Tipo | Regras |
|-------|------|--------|
| usuario_id | integer | PK e FK `usuario` |
| curso | curso (enum) | Obrigatório; restringe a gestão ao próprio curso |

### diretor
| Campo | Tipo | Regras |
|-------|------|--------|
| usuario_id | integer | PK e FK `usuario` |

### administrativo
| Campo | Tipo | Regras |
|-------|------|--------|
| usuario_id | integer | PK e FK `usuario` |

### cpa_externo
| Campo | Tipo | Regras |
|-------|------|--------|
| usuario_id | integer | PK e FK `usuario` |

### dashboard
| Campo | Tipo | Regras |
|-------|------|--------|
| id | integer, identity | Chave primária |
| nome | varchar(255) | Obrigatório |
| url_embed | text | Obrigatório, URL de incorporação |
| ordem | integer | Obrigatório, define a exibição |
| ativo | boolean | Obrigatório |

### dashboard_perfil
| Campo | Tipo | Regras |
|-------|------|--------|
| dashboard_id | integer | FK `dashboard`, parte da PK |
| perfil | perfil (enum) | Parte da PK |

### devolutiva
| Campo | Tipo | Regras |
|-------|------|--------|
| id | integer, identity | Chave primária |
| area | varchar(255) | Obrigatório |
| demanda | text | Obrigatório |
| resposta | text | Obrigatório |
| data_publicacao | date | Preenchida ao publicar |
| status | enum (`rascunho`, `publicada`, `arquivada`) | Obrigatório |
| autor_usuario_id | integer | FK `usuario`, opcional |

### documento
| Campo | Tipo | Regras |
|-------|------|--------|
| id | integer, identity | Chave primária |
| titulo | varchar(255) | Obrigatório |
| categoria | varchar(100) | Obrigatório |
| url_arquivo | text | Obrigatório |
| data_publicacao | date | Obrigatório |
| ativo | boolean | Obrigatório |

### documento_perfil
| Campo | Tipo | Regras |
|-------|------|--------|
| documento_id | integer | FK `documento`, parte da PK |
| perfil | perfil (enum) | Parte da PK |

### canal_contato
| Campo | Tipo | Regras |
|-------|------|--------|
| id | integer, identity | Chave primária |
| nome | varchar(100) | Obrigatório |
| url | text | Obrigatório |
| ordem | integer | Obrigatório |
| ativo | boolean | Obrigatório |

### evento_acesso (auditoria)
| Campo | Tipo | Regras |
|-------|------|--------|
| id | integer, identity | Chave primária |
| usuario_id | integer | FK `usuario`, opcional para acessos públicos |
| recurso | varchar(255) | Obrigatório |
| acao | varchar(50) | Obrigatório |
| resultado | varchar(20) | Obrigatório; `permitido` ou `negado` |
| data_hora | timestamptz | Padrão `now()` |

## Regras de validação
- `email` obrigatório e único; senha sempre armazenada como hash bcrypt.
- Usuário inativo não autentica e não acessa conteúdo restrito.
- `perfil` deve estar entre os seis valores; um usuário pode ter mais de um.
- Coordenador só gerencia cursos do próprio curso (FR-012).
- Base bruta acessível apenas a Diretor e Administrativo (FR-006).
- Dashboard e documento só aparecem se associados a um perfil do usuário (FR-005).
- Devolutiva só é pública quando `status = publicada` (FR-007).
- Sessão expira após 168 horas (FR-010).
- O acesso à base bruta segue FR-006 (Diretor e Administrativo); a divergência com o RNF04 permanece registrada para validação com a CPA.
- Os eventos de auditoria são mantidos por no mínimo 12 meses (FR-013).

## Transições de estado
- Devolutiva: `rascunho` -> `publicada` -> `arquivada`.
- Documento: `ativo` -> `inativo` (sai da listagem, histórico preservado).
- Usuario: `ativo` <-> `inativo`.

## Ajustes necessários no schema atual
1. Remover a dependência circular `usuario.aluno_id` / `aluno.id` e equivalentes;
   as tabelas de perfil devem referenciar `usuario.id`.
2. Adicionar `professor`, `diretor` e vínculo de curso em `coordenador`.
3. Adicionar as tabelas de conteúdo (`dashboard`, `devolutiva`, `documento`,
   `canal_contato`) e as tabelas de permissão (`dashboard_perfil`,
   `documento_perfil`).
4. Renomear `usuario.senha` para `senha_hash` e ajustar `cpf` para `varchar(11)`.
