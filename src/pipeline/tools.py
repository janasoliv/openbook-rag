"""Function-calling / tool-use — registro de tools usadas pelo agente.
"""

from __future__ import annotations

import json
from typing import Any, Callable

def lookup_chapter(chapter: int) -> str:
    """ Retorna o sumário do capítulo informado para apoiar 
    a navegação no livro Pro Git. Para oferece uma resposta mais controlada, rápida e determinística quando a pergunta envolve a organização da obra.
    """

    chapters = {
        1: "Capítulo 1 — Git Basics: apresenta sistemas de controle de versão, conceitos básicos do Git, instalação e configuração inicial.",
        2: "Capítulo 2 — Git Basics: cobre o uso básico do Git, incluindo clone, histórico, modificação de arquivos e contribuição de mudanças.",
        3: "Capítulo 3 — Git Branching: explica o modelo de branches do Git, criação, troca, merge, conflitos e fluxos com branches.",
        4: "Capítulo 4 — Git on the Server: aborda configuração de Git em servidor próprio ou organizacional e opções hospedadas.",
        5: "Capítulo 5 — Distributed Git: apresenta workflows distribuídos, múltiplos repositórios remotos, branches remotos e contribuição com patches.",
        6: "Capítulo 6 — GitHub: explica uso do GitHub, contas, repositórios, contribuição em projetos, pull requests, issues e interface programática.",
        7: "Capítulo 7 — Git Tools: cobre comandos avançados como reset, busca binária para bugs, edição de histórico e seleção de revisões.",
        8: "Capítulo 8 — Customizing Git: trata de configurações, hooks, scripts e políticas personalizadas de commit.",
        9: "Capítulo 9 — Git and Other Systems: explica integração do Git com outros sistemas de controle de versão, especialmente SVN.",
        10: "Capítulo 10 — Git Internals: apresenta funcionamento interno do Git, objetos, modelo de objetos, packfiles e protocolos de servidor."
    }

    return chapters.get(
        chapter,
        "Capítulo não encontrado. Informe um número entre 1 e 10."
    )

# NÃO CONSIDERAR NA AVALIAÇÃO A TOOL ABAIXO, AINDA TÁ SENDO DESENVOLVIDA.
def suggest_study_path(topic: str, level: str = "iniciante") -> str:
    """Sugere uma trilha de estudo no livro Pro Git para um tema específico."""

    topic_key = topic.lower().strip()
    level_key = level.lower().strip()

    paths = {
        "commit": {
            "iniciante": [
                "Capítulo 2 — Entender o fluxo básico: status, add e commit.",
                "Capítulo 7 — Aprofundar em reset, histórico e revisão de commits.",
            ],
            "intermediario": [
                "Capítulo 7 — Estudar edição de histórico, reset e seleção de revisões.",
                "Capítulo 8 — Ver hooks e políticas de commit.",
            ],
        },
        "branch": {
            "iniciante": [
                "Capítulo 2 — Revisar o fluxo básico de trabalho no Git.",
                "Capítulo 3 — Estudar criação, troca, merge e conflitos de branches.",
            ],
            "intermediario": [
                "Capítulo 3 — Aprofundar em branching e merge.",
                "Capítulo 5 — Estudar branches remotos e workflows distribuídos.",
            ],
        },
        "github": {
            "iniciante": [
                "Capítulo 6 — Estudar criação de repositórios, forks, issues e pull requests.",
            ],
            "intermediario": [
                "Capítulo 5 — Revisar colaboração distribuída.",
                "Capítulo 6 — Aprofundar em contribuição e revisão de código no GitHub.",
            ],
        },
        "internals": {
            "iniciante": [
                "Capítulo 10 — Introdução aos objetos internos do Git.",
            ],
            "intermediario": [
                "Capítulo 10 — Estudar objetos, trees, blobs, commits, packfiles e referências.",
            ],
        },
    }

    if topic_key not in paths:
        return (
            "Tema não encontrado na trilha pré-definida. "
            "Use o RAG para buscar o tema no livro Pro Git."
        )

    steps = paths[topic_key].get(level_key, paths[topic_key]["iniciante"])

    return "\n".join(
        [f"Trilha sugerida para '{topic}' ({level_key}):"]
        + [f"{i+1}. {step}" for i, step in enumerate(steps)]
    )

TOOLS: list[dict[str, Any]] = [
    # SEU CODIGO AQUI — TODO 4 (continuacao)
    {
        "type": "function",
        "function": {
            "name": "lookup_chapter",
            "description": (
                "Consulta um resumo curto de um capitulo do livro Pro Git/GitPro. "
                "Use esta tool quando a pergunta mencionar um capitulo especifico "
                "ou quando for necessario localizar o tema geral de uma parte do livro. "
                "A resposta final deve usar o corpus indexado para incluir citação de página."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "chapter": {
                        "type": "integer",
                        "description": "Numero do capitulo do livro, entre 1 e 10."
                    }
                },
                "required": ["chapter"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "suggest_study_path",
            "description": (
                "Sugere uma trilha de estudo no livro Pro Git para um tema específico, "
                "indicando capítulos e ordem recomendada de leitura."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Tema de Git que o usuário deseja estudar, como commit, branch, github ou internals."
                    },
                    "level": {
                        "type": "string",
                        "description": "Nível do usuário: iniciante ou intermediario."
                    }
                },
                "required": ["topic"]
            }
        }
    }
]

TOOL_REGISTRY: dict[str, Callable[..., str]] = {
    "lookup_chapter": lookup_chapter,
    "suggest_study_path": suggest_study_path,
}


def run_tool_call(name: str, arguments_json: str) -> str:
    """Executa uma tool call e retorna o resultado como string."""
    if name not in TOOL_REGISTRY:
        return f"ERROR: tool '{name}' nao registrada"
    try:
        kwargs = json.loads(arguments_json)
        return TOOL_REGISTRY[name](**kwargs)
    except Exception as e:
        return f"ERROR ao executar {name}: {e}"
