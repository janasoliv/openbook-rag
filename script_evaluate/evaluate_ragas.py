from __future__ import annotations

import os
import sys
from pathlib import Path

from datasets import Dataset
from dotenv import load_dotenv
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

# Permite importar src.pipeline.rag quando o script é executado da raiz do projeto
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.pipeline.rag import build_rag_pipeline  # noqa: E402


load_dotenv()


GOLDEN_SET = [
    {
        "question": "O que é Git?",
        "ground_truth": (
            "Git é um sistema distribuído de controle de versão usado para rastrear "
            "alterações em arquivos e coordenar o trabalho em projetos."
        ),
    },
    {
        "question": "O que é um commit no Git?",
        "ground_truth": (
            "Um commit registra um snapshot das alterações preparadas no repositório, "
            "criando um ponto no histórico do projeto."
        ),
    },
    {
        "question": "Para que serve o git clone?",
        "ground_truth": (
            "O git clone cria uma cópia local de um repositório existente, incluindo "
            "seu histórico e referências principais."
        ),
    },
    {
        "question": "Para que serve uma branch no Git?",
        "ground_truth": (
            "Uma branch permite trabalhar em uma linha separada de desenvolvimento, "
            "facilitando alterações paralelas sem afetar diretamente a linha principal."
        ),
    },
    {
        "question": "O que acontece em um merge?",
        "ground_truth": (
            "Um merge combina alterações de uma branch em outra, integrando históricos "
            "e podendo gerar conflitos quando as mesmas partes de arquivos foram alteradas."
        ),
    },
    {
        "question": "Qual é a diferença entre git fetch e git pull?",
        "ground_truth": (
            "O git fetch baixa alterações do repositório remoto sem integrá-las automaticamente, "
            "enquanto o git pull baixa e tenta integrar essas alterações à branch atual."
        ),
    },
    {
        "question": "O que é um repositório remoto no Git?",
        "ground_truth": (
            "Um repositório remoto é uma versão do projeto hospedada em outro local, usada "
            "para colaboração, envio e recebimento de alterações."
        ),
    },
    {
        "question": "Para que serve o GitHub no contexto do livro Pro Git?",
        "ground_truth": (
            "O GitHub é apresentado como uma plataforma de hospedagem e colaboração em "
            "repositórios Git, com recursos como forks, pull requests e issues."
        ),
    },
    {
        "question": "O que é o comando git reset?",
        "ground_truth": (
            "O git reset é um comando usado para mover referências e alterar o estado do índice "
            "e da árvore de trabalho, dependendo do modo utilizado."
        ),
    },
    {
        "question": "O que são objetos internos do Git?",
        "ground_truth": (
            "Objetos internos do Git são estruturas usadas para armazenar dados e histórico, "
            "incluindo blobs, trees, commits e tags."
        ),
    },
]


def main() -> None:
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError("Configure OPENAI_API_KEY ou GEMINI_API_KEY no .env")

    pipeline = build_rag_pipeline(corpus_dir=str(ROOT / "data" / "corpus"))

    records = []

    for item in GOLDEN_SET:
        question = item["question"]

        result = pipeline.answer(question, k=5)
        hits = pipeline.retrieve(pipeline.rewrite_query(question), k=5)

        records.append(
            {
                "question": question,
                "answer": result["answer"],
                "contexts": [hit["text"] for hit in hits],
                "ground_truth": item["ground_truth"],
            }
        )

    dataset = Dataset.from_list(records)

    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
        ],
    )

    df = result.to_pandas()

    # Salva o resultado completo em CSV
    output_dir = ROOT / "script_evaluate" / "results"
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "ragas_results.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(f"- CSV: {csv_path}")

    faith = df["faithfulness"].mean()
    ans_rel = df["answer_relevancy"].mean()
    ctx_prec = df["context_precision"].mean()

    print("\nResultados por pergunta:")
    print(df[["question", "faithfulness", "answer_relevancy", "context_precision"]])

    print("\nResultados finais:")
    print(
        f"faithfulness={faith:.2f}, "
        f"answer_relevancy={ans_rel:.2f}, "
        f"context_precision={ctx_prec:.2f}"
    )


if __name__ == "__main__":
    main()