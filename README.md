# Portal CPA: Transparência e Comunicação na Avaliação Institucional
_**Em contrução**_
## Objetivo
Desenvolver um portal web para a CPA que centralize e apresente, de forma estruturada e com controle de acesso, os dashboards das pesquisas institucionais, as devolutivas das áreas e os relatórios, possibilitando que alunos, coordenadores, avaliadores externos e a comunidade em geral acessem as informações pertinentes ao seu perfil, promovendo transparência e melhoria contínua.

**Público alvo:** Alunos, coordenadores de cursos, direção, avaliadores externos e demais membros da faculdade

## Funcionalidades
- **Sistema de login com níveis de acesso:** Perfis de aluno, coordenador, administrador (CPA) e avaliador externo.
- **Página inicial com dashboards:** Exibição dos dashboards do Google Data Studio de acordo com o perfil do usuário (alunos: pesquisa da CPA; coordenadores: pesquisas da CPA, avaliação docente e egressos; avaliador externo: acesso total).
- **Mural de devolutivas:** página pública onde são publicadas as resoluções e respostas das áreas às demandas levantadas nas pesquisas da CPA.
- **Área de relatórios e boletins:** repositório de documentos institucionais, como relatórios de autoavaliação e boletins informativos.
- **Página de contato:** espaço para interação com a CPA, com links para Google Chats e Google Meet.

## Tecnologias utilizadas
- Desenvolvimento web: Streamlit (Lib do python)
- Backend: Python
- Banco de dados: Postgres
- Dashboards: Google Data Studio

## Etapas do projeto
- [x] Levantamento de requisitos com a CPA.
- [x] Modelagem do banco de dados e criação dos perfis de acesso.
- [x] Desenvolvimento do portal e integração dos dashboards.
- [ ] Criação do mural de devolutivas e área de relatórios.
- [ ] Testes e validação com usuários reais.
- [ ] Implantação e treinamento dos usuários.


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
- coordenador@exemplo.com
- administrativo@exemplo.com
- externo@exemplo.com

## Criacao de usuarios

Somente um usuario com cargo Administrativo pode criar usuarios. Na pagina
Administracao, informe nome, e-mail, senha, um ou mais cargos e, opcionalmente,
CPF. O usuario e criado sempre ativo.

Observacao: o CPF e normalizado para apenas digitos (pontos e traco sao
removidos) e gravado na coluna `usuario.cpf`, que e `VARCHAR(11)`. O valor
completo de 11 digitos e preservado, inclusive zeros a esquerda.

## Recuperacao de senha e sessao

Na tela de login, a opcao "Esqueci minha senha" abre um formulario com e-mail, nova
senha e confirmacao. O pedido fica pendente e so e aplicado quando um usuario
Administrativo aprova, na pagina Administracao. Recusas e pedidos com mais de 24
horas nao alteram a senha.

A mensagem exibida apos o envio e a mesma para e-mail existente e inexistente, para
nao revelar quais contas estao cadastradas.

Depois do login, o portal guarda a sessao em um cookie assinado, `portal_cpa_sessao`,
valido por 168 horas (uma semana) a partir daquele login. Recarregar a pagina ou
reabrir o navegador mantem o usuario autenticado; "Sair" remove o cookie. A sessao e
revalidada a cada carga e deixa de valer se o usuario for desativado.

O schema agora inclui a tabela `solicitacao_senha`; bancos criados antes desta
feature precisam de volume novo (`docker compose down -v`).


## Estrutura

- `src/main.py`: entrada, autenticacao e navegacao
- `src/auth`: autenticacao e permissoes
- `src/data`: conexao, modelos e repositorios
- `src/views`: paginas
- `src/ui`: layout compartilhado
- `database`: schema e dados iniciais
