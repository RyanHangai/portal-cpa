# UI Contract: Cadastro de Usuário

## Página: Administração - Criar usuário

- View: `src/views/administracao.py`
- Autenticação: obrigatória
- Perfis com acesso: somente Administrativo
- Visibilidade: a seção de cadastro não aparece para Coordenador, Aluno ou CPA
  Externo; acesso direto é negado.

## Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Nome | texto | sim | |
| E-mail | texto | sim | Verificado como único |
| Senha | texto (oculto) | sim | Mínimo de 8 caracteres |
| Cargos | seleção múltipla | sim | Pelo menos um; Aluno, Coordenador, Administrativo, CPA Externo |
| Curso | seleção | sim, quando Aluno selecionado | Ciência da Computação, Engenharia de Software, Análise de Sistemas, Sistema da Informação |
| CPF | texto | não | Quando informado, 11 dígitos; pontos e traço são removidos e apenas os dígitos são gravados em `VARCHAR(11)` |

## Estados

- Sucesso: mensagem de confirmação e o usuário aparece na lista.
- Erro de validação: mensagem específica ao lado do formulário, sem criar usuário.
- Erro de e-mail duplicado: mensagem clara, sem criar usuário.
- Sem cargo selecionado: mensagem de cargo obrigatório.
- Cargo Aluno sem curso: mensagem de curso obrigatório.

## Regras de segurança
- A senha não é exibida após a criação.
- A seção só é renderizada para Administrativo, além da guarda de acesso.
