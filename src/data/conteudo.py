"""Conteudo estatico que o schema atual nao armazena em tabelas."""
from __future__ import annotations

DASHBOARDS = [
    {
        "nome": "Pesquisa - Professores",
        "url_embed": "https://datastudio.google.com/embed/reporting/ee6a7999-c41a-41e7-9c73-2ac0fff59d49/page/p_k1tjc7bebd",
        "ordem": 1,
        "perfis": ["coordenador", "cpa_externo"],
    },
    {
        "nome": "Pesquisa - Aluno Presencial",
        "url_embed": "https://datastudio.google.com/embed/reporting/c6fac40f-46c9-489d-a63f-653537ca5719/page/p_k1tjc7bebd",
        "ordem": 2,
        "perfis": ["aluno", "coordenador", "cpa_externo"],
    },
    {
        "nome": "Pesquisa - Aluno EAD",
        "url_embed": "https://datastudio.google.com/embed/reporting/a29dac9a-c940-4eec-9d63-7d811debf2ec/page/p_k1tjc7bebd",
        "ordem": 3,
        "perfis": ["aluno", "coordenador", "cpa_externo"],
    },
    {
        "nome": "Pesquisa - Administracao",
        "url_embed": "https://datastudio.google.com/embed/reporting/d1cfe171-e39a-47bd-abc1-c131be08d632/page/p_k1tjc7bebd",
        "ordem": 4,
        "perfis": ["administrativo", "coordenador", "cpa_externo"],
    },
]

CANAIS_CONTATO = [
    {"nome": "Google Chats da CPA", "url": "https://chat.google.com/", "ordem": 1},
    {"nome": "Google Meet da CPA", "url": "https://meet.google.com/", "ordem": 2},
]
