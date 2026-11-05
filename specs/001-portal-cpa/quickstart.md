# Quickstart: Validação do Portal CPA

## Pré-requisitos
- Docker e Docker Compose instalados.
- Arquivo `.env` na raiz com as credenciais do banco e o segredo do cookie.

## Subir o ambiente
Na primeira execução, ou ao alterar o schema:

```sh
docker compose down -v
docker compose up -d --build
docker compose logs -f app
```

Endereços:
- Aplicação: http://localhost:8002
- PostgreSQL: localhost:8001

## Conferir o schema
```sh
docker compose exec postgres psql -U postgres -d postgres -c "\dt"
```

## Cenários de validação

### 1. Login e direcionamento por perfil (US1)
- Entrar com um usuário de cada perfil.
- Esperado: página inicial compatível com o perfil; acesso direto a página restrita
  é bloqueado; credenciais inválidas exibem erro.

### 2. Dashboards por perfil (US2)
- Autenticar como Aluno, Coordenador e CPA Externo.
- Esperado: cada perfil vê apenas os dashboards permitidos; os demais não aparecem
  e não abrem por endereço direto.

### 3. Mural de devolutivas público (US3)
- Abrir o mural sem autenticação.
- Esperado: devolutivas publicadas visíveis, com área, demanda, resposta e data.

### 4. Relatórios e boletins (US4)
- Autenticar com perfis diferentes e abrir a área de relatórios.
- Esperado: cada perfil vê apenas os documentos permitidos e consegue abri-los.

### 5. Página de contato (US5)
- Abrir a página sem autenticação.
- Esperado: canais oficiais exibidos e redirecionando corretamente.

### 6. Expiração de sessão (FR-010)
- Simular cookie com data além de 168 horas.
- Esperado: sessão encerrada e login exigido.

## Testes automatizados
```sh
docker compose exec app pytest
```

Esperado: testes de unidade, de integração e de fluxo de tela aprovados, com
cobertura das regras de permissão.
