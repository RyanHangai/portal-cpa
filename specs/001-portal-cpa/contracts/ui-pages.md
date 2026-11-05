# UI Contracts: Páginas do Portal

## Login
- View: `src/main.py` (gate de autenticação)
- Autenticação: pública
- Entradas: e-mail e senha
- Saída: sessão autenticada com cookie de 7 dias
- Erros: credenciais inválidas, usuário inativo

## Início / Dashboards
- View: `src/views/dashboards.py`
- Autenticação: obrigatória
- Perfis: todos os autenticados, com conteúdo filtrado por perfil
- Dados: dashboards associados aos perfis do usuário, ordenados por `ordem`
- Estados: lista vazia exibe mensagem; embed indisponível exibe link direto

## Devolutivas (público)
- View: `src/views/devolutivas.py`
- Autenticação: pública
- Dados: devolutivas com `status = publicada`
- Estados: lista vazia exibe mensagem

## Relatórios e boletins
- View: `src/views/relatorios.py`
- Autenticação: obrigatória
- Dados: documentos visíveis aos perfis do usuário
- Ações: abrir e baixar documento

## Contato
- View: `src/views/contato.py`
- Autenticação: pública
- Dados: canais oficiais ativos, ordenados por `ordem`

## Administração
- View: `src/views/administracao.py`
- Autenticação: obrigatória
- Perfis: Administrativo e Diretor; Coordenador restrito ao próprio curso
- Ações: gerenciar usuários, cursos e publicar conteúdo

## Regra transversal de acesso
- Toda view restrita valida autenticação e perfil antes de renderizar dados.
- Página não permitida ao perfil não aparece na navegação e, se acessada por
  endereço direto, é bloqueada (FR-005).
