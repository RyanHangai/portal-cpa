# Data Access Contracts

## Repositório de usuários (`src/data/repositories/usuarios.py`)
- `buscar_por_email(email: str) -> Usuario | None`
- `listar_por_perfil(perfil: str) -> list[Usuario]`
- `criar_usuario(dados: DadosNovoUsuario) -> Usuario`
- `definir_ativo(usuario_id: int, ativo: bool) -> None`

## Repositório de dashboards (`src/data/repositories/dashboards.py`)
- `listar_para_perfis(perfis: list[str]) -> list[Dashboard]`

## Repositório de devolutivas (`src/data/repositories/devolutivas.py`)
- `listar_publicadas() -> list[Devolutiva]`

## Repositório de documentos (`src/data/repositories/documentos.py`)
- `listar_para_perfis(perfis: list[str]) -> list[Documento]`

## Repositório de contatos (`src/data/repositories/contatos.py`)
- `listar_ativos() -> list[CanalContato]`

## Auditoria (`src/data/repositories/eventos.py`)
- `registrar_evento(usuario_id: int | None, recurso: str, acao: str) -> None`

## Erros esperados
- `RegistroNaoEncontrado`
- `PermissaoNegada`
- `BancoIndisponivel`

## Regras
- Toda consulta usa parâmetros vinculados; nunca concatenar valores em SQL.
- Repositórios não conhecem detalhes de interface; retornam modelos de domínio.
