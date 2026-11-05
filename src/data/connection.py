"""Conexao com o PostgreSQL usando um pool do psycopg."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from config import database_config

_pool: ConnectionPool | None = None


def _obter_pool() -> ConnectionPool:
    global _pool
    if _pool is None:
        _pool = ConnectionPool(
            conninfo=database_config().conninfo(),
            min_size=1,
            max_size=5,
            kwargs={"row_factory": dict_row},
            open=False,
        )
        _pool.open()
    return _pool


@contextmanager
def conectar() -> Iterator:
    with _obter_pool().connection() as conexao:
        yield conexao
