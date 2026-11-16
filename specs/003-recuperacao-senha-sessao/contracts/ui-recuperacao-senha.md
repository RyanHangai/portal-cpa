# UI Contract: Recuperação de Senha

## Tela de login (`src/main.py`)

- Autenticação: não exigida.
- A barra lateral mantém o formulário de login e acrescenta um expansor
  "Esqueci minha senha" com:

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| E-mail | texto | sim | Comparado sem maiúsculas nem espaços nas pontas |
| Nova senha | texto oculto | sim | Mínimo de 8 caracteres |
| Confirmação da nova senha | texto oculto | sim | Igual à nova senha |

- Ação: "Solicitar troca de senha".
- Estados:
  - Pedido enviado: mensagem neutra "Se os dados estiverem corretos, o pedido sera
    analisado por um Administrativo.".
  - Erro de campo obrigatório, senha curta ou confirmação divergente: mensagem específica,
    sem registrar pedido.
  - Banco indisponível: mensagem de indisponibilidade, sem registrar pedido.

## Página Administração (`src/views/administracao.py`)

- Autenticação: obrigatória.
- Visibilidade: somente cargos com `administrativo`; os demais não veem a seção.
- Seção "Solicitações de senha":
  - Lista com e-mail do solicitante e momento do pedido.
  - Botões "Aprovar" e "Recusar" por linha.
  - Lista vazia exibe aviso de que não há solicitações pendentes.
- Após aprovar ou recusar, a lista é recarregada e uma mensagem de confirmação é exibida.
- A senha solicitada nunca é exibida.

## Regras de segurança

- A mensagem do envio não revela se o e-mail está cadastrado.
- As ações de listar, aprovar e recusar não aparecem para cargos diferentes de
  Administrativo.
- Nenhuma tela mostra a senha do usuário.
