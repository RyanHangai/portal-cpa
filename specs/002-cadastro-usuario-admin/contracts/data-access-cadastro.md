# Data Access Contract: Cadastro de Usuário

## Repositório (`src/data/repositories/usuarios.py`)

- `criar_usuario_com_cargos(dados: DadosCadastroUsuario) -> Usuario`
  - Cria o usuário e vincula um ou mais cargos em uma única transação.
  - Retorna o usuário criado com situação ativa.
- `buscar_por_email(email: str) -> Usuario | None`
  - Já existente; usado para a checagem de e-mail duplicado.

## Erros esperados

- `EmailDuplicado`
- `DadosInvalidos`
- `BancoIndisponivel`

## Regras

- Toda consulta usa parâmetros vinculados.
- A criação é atômica: se um cargo falhar, nada é gravado.
- O id do usuário é reaproveitado como id da tabela de perfil do cargo.
- A senha é gravada na coluna `senha` conforme o schema atual.
