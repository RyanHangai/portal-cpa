# Research: Portal de Transparência da CPA

## Decisões

### R1. Framework de interface
- Decision: Streamlit, em aplicação multipágina com `st.navigation` e `st.Page`.
- Rationale: já é a stack do projeto (`requirements.txt`) e permite montar a
  navegação a partir do perfil, escondendo páginas não permitidas.
- Alternatives considered: Flask ou Django (mais estrutura e troca de stack);
  Dash (foco em gráficos, não em conteúdo institucional).

### R2. Autenticação e sessão
- Decision: `streamlit-authenticator` com cookie JWT, hashes bcrypt e expiração de
  7 dias (168 horas).
- Rationale: entrega login, controle de tentativas e cookie de sessão sem
  reimplementar criptografia.
- Alternatives considered: autenticação própria com bcrypt e cookies (mais código e
  mais risco de erro); OIDC nativo do Streamlit (exige provedor externo, fora do
  escopo).
- Note: as credenciais são lidas do PostgreSQL, e não do arquivo YAML padrão da
  biblioteca.

### R3. Acesso a dados
- Decision: psycopg 3 com SQL parametrizado, organizado em repositórios por
  entidade.
- Rationale: consultas explícitas e legíveis; poucas dependências; alinhado à
  constituição.
- Alternatives considered: SQLAlchemy ORM (mais abstração); acesso direto nas telas
  (viola a separação de responsabilidades).

### R4. Modelo de perfis e permissões
- Decision: enum `perfil` e tabela `usuario_perfil`, permitindo mais de um perfil
  por usuário.
- Rationale: cobre o edge case de múltiplos perfis e mantém as permissões
  explícitas.
- Alternatives considered: coluna única `perfil` em `usuario` (não cobre múltiplos
  perfis).

### R5. Dashboards
- Decision: incorporar URLs de embed do Google Looker Studio em iframe, com
  metadados (nome, URL, perfis permitidos) no banco.
- Rationale: os painéis já existem e são mantidos pela instituição; o portal apenas
  os apresenta. Os links atuais estão em
  `levantamento_requisitos/dashboard.md`.
- Alternatives considered: recriar os gráficos (fora do escopo); abrir em nova aba
  (pior experiência).
- Fallback: quando o embed falhar, exibir link direto e mensagem clara.

### R6. Ciclo de vida do schema
- Decision: manter `database/database.sql` como bootstrap via
  `/docker-entrypoint-initdb.d`, mas normalizar o schema antes da implementação.
- Rationale: o arquivo atual tem relações circulares (`usuario` aponta para
  `aluno`/`coordenador` e vice-versa) e não cobre Professor e Diretor.
- Alternatives considered: adotar ferramenta de migração agora (goose/Flyway),
  possível, mas adiada para não ampliar o escopo.
- Risk: o initdb.d só roda em volume vazio; mudanças de schema exigem
  `docker compose down -v`.

### R7. Configuração e segredos
- Decision: variáveis de ambiente no Compose e `.env` local (não versionado);
  segredo de cookie obrigatório.
- Rationale: evita credenciais fixas e mantém a configuração fora do código.

### R8. Estratégia de testes
- Decision: pytest para unidades e integração; `AppTest` para fluxos de tela; banco
  de teste descartável.
- Rationale: cobre a lógica de permissões e o comportamento das telas sem depender
  de navegador real.

### R9. Conflito de requisitos sobre base bruta
- Decision: seguir a spec (FR-006): base bruta acessível apenas a Diretor e
  Administrativo.
- Rationale: a spec é a fonte de verdade do planejamento.
- Note: `levantamento_requisitos/requisitos.md` (RNF04) contradiz ao excluir o
  Diretor; registrar para validação com a CPA.

## Unknowns residuais

Nenhuma pendência bloqueante. As decisões acima resolvem os pontos em aberto da
especificação.
