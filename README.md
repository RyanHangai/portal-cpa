# Portal CPA

Portal web para a CPA que centraliza, com controle de acesso por perfil, os
dashboards das pesquisas institucionais, o mural de devolutivas, os relatorios e
os canais de contato.

## Tecnologias

- Python 3.14 e Streamlit
- PostgreSQL 18
- Docker Compose

## Como rodar

Suba os servicos:

```sh
docker compose up -d --build
```

Enderecos:

- Aplicacao: http://localhost:8002
- PostgreSQL: localhost:8001

O schema e os dados de exemplo sao aplicados apenas na primeira criacao do
volume. Para recriar do zero:

```sh
docker compose down -v
```

## Contas de exemplo

Todas usam a senha `senha123`.

- aluno@exemplo.com
- professor@exemplo.com
- coordenador@exemplo.com
- diretor@exemplo.com
- administrativo@exemplo.com
- externo@exemplo.com

## Testes

```sh
docker compose exec app pytest
```

## Estrutura

- `src/main.py`: entrada, autenticacao e navegacao
- `src/auth`: autenticacao e permissoes
- `src/data`: conexao, modelos e repositorios
- `src/views`: paginas
- `src/ui`: layout compartilhado
- `database`: schema e dados iniciais
- `specs/001-portal-cpa`: especificacao, plano e tarefas
