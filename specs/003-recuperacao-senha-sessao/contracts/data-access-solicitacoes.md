# Contract: Acesso a Dados das Solicitações de Senha

## Módulo `src/data/repositories/solicitacoes.py`

- `registrar_solicitacao_senha(email: str, nova_senha: str) -> bool`
  - Normaliza o e-mail e busca um usuário ativo.
  - Remove o pedido `pendente` anterior do mesmo usuário.
  - Insere a nova solicitação com `situacao = 'pendente'`.
  - Devolve `True` quando registrou, `False` quando o e-mail não pertence a conta ativa.
- `listar_solicitacoes_pendentes() -> list[SolicitacaoSenha]`
  - Marca como `expirada` as pendentes com mais de 24 horas.
  - Devolve as pendentes restantes em ordem de `criado_em`.
- `aprovar_solicitacao(solicitacao_id: int, administrador_id: int) -> bool`
  - Aprova somente se a situação for `pendente` e aplica a `nova_senha` em `usuario.senha`.
  - Devolve `False` quando a solicitação já foi decidida.
- `recusar_solicitacao(solicitacao_id: int, administrador_id: int) -> bool`
  - Recusa somente se a situação for `pendente`; não altera `usuario.senha`.
  - Devolve `False` quando a solicitação já foi decidida.

## Módulo `src/data/repositories/usuarios.py`

- `buscar_por_id(usuario_id: int) -> Usuario | None`
  - Já existente na prática por `buscar_por_email`; acrescentado para restaurar a sessão.

## Erros esperados

- `BancoIndisponivel`
- `DadosInvalidos`

## Regras

- Toda operação usa parâmetros vinculados.
- Aprovar executa duas atualizações na mesma transação: a solicitação e a senha.
- Nenhuma função de leitura expõe `nova_senha` para a interface.
- A decisão de um Administrativo grava `decidido_por` e `decidido_em`.
- A expiração grava `situacao = 'expirada'` e deixa `decidido_por` nulo.

## Modelo de leitura

```python
@dataclass(frozen=True)
class SolicitacaoSenha:
    id: int
    usuario_id: int
    email: str
    criado_em: datetime
    situacao: str
```

`nova_senha` não faz parte do modelo devolvido à interface.
