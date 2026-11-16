# Quickstart: Cadastro de Usuário pelo Administrativo

## Pré-requisitos

- Stack no ar (`docker compose up -d --build`).
- Um usuário com cargo Administrativo existente para entrar no sistema.

## Como validar

1. Acesse `http://localhost:8002` e faça login como Administrativo.
2. Abra a página Administração.
3. Use o formulário de criar usuário.

## Cenários

### 1. Criar um usuário Coordenador
- Preencha nome, e-mail novo, senha com 8 ou mais caracteres e selecione o cargo
  Coordenador.
- Esperado: confirmação na tela e usuário na lista.
- Valide o login com o e-mail e a senha cadastrados.

### 2. Criar um usuário Aluno
- Preencha os dados, selecione o cargo Aluno e escolha um curso.
- Esperado: usuário criado com o curso vinculado.
- Tente criar um Aluno sem curso e confirme a mensagem de curso obrigatório.

### 3. Criar um usuário Administrativo
- Preencha os dados e selecione o cargo Administrativo.
- Esperado: usuário criado e apto a acessar a administração.

### 4. Criar um usuário CPA Externo
- Preencha os dados e selecione o cargo CPA Externo.
- Esperado: usuário criado com acesso aos dashboards permitidos.

### 5. Criar um usuário com mais de um cargo
- Selecione, por exemplo, Coordenador e CPA Externo.
- Esperado: usuário criado com os dois vínculos.

### 6. Validações
- Enviar sem cargo: mensagem de cargo obrigatório.
- Enviar com e-mail já cadastrado: mensagem de e-mail duplicado, sem criar.
- Enviar com senha curta: mensagem de senha mínima.
- Enviar com CPF fora de 11 dígitos: mensagem de CPF inválido.

### 7. Controle de acesso
- Entrar como Coordenador, Aluno ou CPA Externo e conferir que a seção de cadastro
  não aparece.
- Tentar acessar a criação por endereço direto e confirmar o bloqueio.

## Testes automatizados

```sh
docker compose exec app pytest
```

Esperado: testes unitários e de integração do cadastro aprovados, além dos testes
existentes.
