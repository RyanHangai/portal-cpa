# Quickstart: Recuperação de Senha e Sessão Persistente

## Pré-requisitos

- Stack no ar com o volume recriado, porque o schema ganhou a tabela `solicitacao_senha`:
  `docker compose down -v` e depois `docker compose up -d --build`.
- Um usuário Administrativo (`administrativo@exemplo.com`) e um usuário comum
  (`aluno@exemplo.com`), ambos com senha `senha123`.

## Como validar

1. Acesse `http://localhost:8002`.
2. Abra o expansor "Esqueci minha senha" na barra lateral.

## Cenários

### 1. Solicitar troca com dados válidos
- Informe o e-mail `aluno@exemplo.com`, a nova senha `novaSenha123` e a mesma confirmação.
- Esperado: mensagem neutra de pedido enviado; o login com `senha123` continua funcionando.

### 2. Aprovar a solicitação
- Entre como `administrativo@exemplo.com`.
- Abra Administração e localize a solicitação de `aluno@exemplo.com`.
- Aprove.
- Esperado: a lista fica sem a solicitação e o login de `aluno@exemplo.com` passa a valer
  com `novaSenha123` e a falhar com `senha123`.

### 3. Recusar a solicitação
- Repita o cenário 1 com outro e-mail e recuse o pedido.
- Esperado: a senha antiga continua valendo e a senha do pedido falha no login.

### 4. Confirmação divergente e senha curta
- Envie a recuperação com confirmação diferente e, depois, com senha de 7 caracteres.
- Esperado: mensagem específica em cada caso, sem registrar pedido.

### 5. E-mail inexistente
- Envie a recuperação para `ninguem@exemplo.com`.
- Esperado: a mesma mensagem neutra do cenário 1 e nenhuma solicitação na lista do
  Administrativo.

### 6. Sessão de uma semana
- Entre com qualquer conta e recarregue a página.
- Esperado: continua autenticado.
- Feche e reabra o navegador dentro do prazo.
- Esperado: continua autenticado.
- Confira no navegador o cookie `portal_cpa_sessao`, com validade de 168 horas.

### 7. Sair
- Acione "Sair".
- Esperado: volta ao login e o cookie `portal_cpa_sessao` deixa de existir.
- Recarregue a página.
- Esperado: continua no login.

### 8. Sessão inválida
- Com a sessão ativa, altere o valor do cookie no navegador.
- Recarregue a página.
- Esperado: volta ao login, sem mensagem de erro técnico.

## Testes automatizados

```sh
docker compose exec app pytest
```

Esperado: testes de unidade do token de sessão e da validação, testes de integração das
solicitações e AppTest da tela de login aprovados, além dos testes existentes.

> `docker compose down -v` apaga o volume. Sem recriar o volume, a tabela nova não existe e
> as operações de recuperação falham com erro de banco.
