"""Configuracao da aplicacao lida de variaveis de ambiente."""
from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_COOKIE_SECRET = "dev-secret-nao-use-em-producao"


@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: str
    password: str

    def conninfo(self) -> str:
        return (
            f"host={self.host} port={self.port} dbname={self.name} "
            f"user={self.user} password={self.password}"
        )


def database_config() -> DatabaseConfig:
    return DatabaseConfig(
        host=os.environ.get("DB_HOST", "postgres"),
        port=int(os.environ.get("DB_PORT", "5432")),
        name=os.environ.get("DB_NAME", "postgres"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres"),
    )


def cookie_secret() -> str:
    return os.environ.get("COOKIE_SECRET", DEFAULT_COOKIE_SECRET)
