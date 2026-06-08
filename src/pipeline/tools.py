"""Function-calling / tool-use — registro de tools usadas pelo agente.
"""

from __future__ import annotations

import json
from typing import Any, Callable


# ============================================================================
# TODO 4 — Sua tool especifica do dominio
# ============================================================================
# Cada projeto precisa de UMA tool customizada que faca sentido para o problema.
# Exemplos por dominio:
#   - Livro tecnico:    lookup_chapter(chapter: int) -> str
#   - Changelog:        check_compat(lib: str, version: str) -> dict
#   - Podcast:          get_timestamp(quote: str) -> str
#   - Codigo:           run_snippet(code: str) -> str  (sandboxed)
#   - Documentos legais: cite_article(law: str, article: int) -> str
#
# 1. Implemente a funcao Python real abaixo (substitua o exemplo)
# 2. Adicione o schema JSON em TOOLS abaixo
# 3. Registre em TOOL_REGISTRY
# ============================================================================


# SEU CODIGO AQUI — TODO 4
# def my_domain_tool(arg1: str) -> str:
#     """Substitua esta funcao pela sua tool especifica.

#     A funcao deve receber argumentos primitivos (str, int, float, bool) e
#     retornar string com o resultado (sera passado de volta ao LLM como tool result).
#     """
#     return f"TODO: implementar tool para o argumento: {arg1}"

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
]

TOOL_REGISTRY: dict[str, Callable[..., str]] = {
    # "my_domain_tool": my_domain_tool,
    "lookup_chapter": lookup_chapter,
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
