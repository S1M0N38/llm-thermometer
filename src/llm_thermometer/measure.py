"""Module for measuring semantic similarity of multiple samples."""

import logging
import os
from argparse import Namespace
from collections import defaultdict
from itertools import combinations

from openai import AsyncOpenAI
from tqdm import tqdm

from llm_thermometer.models import Embedding, Sample, Similarity

BATCH_SIZE = 16

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

assert (EMB_API_KEY := os.getenv("EMB_API_KEY", ""))
assert (EMB_BASE_URL := os.getenv("EMB_BASE_URL", ""))


def cosine_similarity(emb1: Embedding, emb2: Embedding) -> Similarity:
    """Calculate cosine similarity between two vectors."""
    assert emb1.model == emb2.model
    model = emb1.model
    vec1, vec2 = emb1.embedding, emb2.embedding
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = sum(a * a for a in vec1) ** 0.5
    norm_b = sum(b * b for b in vec2) ** 0.5
    result = dot_product / (norm_a * norm_b)

    return Similarity(
        model=model,
        sample_id1=emb1.sample_id,
        sample_id2=emb2.sample_id,
        similarity=result,
    )


async def generate_embeddings(
    model: str,
    samples: list[Sample],
) -> list[Embedding]:
    client = AsyncOpenAI(api_key=EMB_API_KEY, base_url=EMB_BASE_URL)
    samples_batches = [
        samples[i : i + BATCH_SIZE] for i in range(0, len(samples), BATCH_SIZE)
    ]

    embeddings: list[Embedding] = []
    for samples_batch in tqdm(samples_batches, desc="Embeddings"):
        response = await client.embeddings.create(
            input=[sample.completion for sample in samples_batch],
            model=model,
        )
        embeddings.extend(
            [
                Embedding(
                    model=model,
                    sample_id=sample.id,
                    embedding=emb.embedding,
                )
                for sample, emb in zip(samples_batch, response.data)
            ]
        )

    await client.close()
    assert len(embeddings) == len(samples), (
        "Number of embeddings does not match number of samples"
    )
    return embeddings


def pair_embeddings(
    samples: list[Sample], embeddings: list[Embedding]
) -> list[tuple[Embedding, Embedding]]:
    sample_id_to_temp = {sample.id: sample.temperature for sample in samples}

    temp_to_embeddings = defaultdict(list)
    for emb in embeddings:
        temp_to_embeddings[sample_id_to_temp[emb.sample_id]].append(emb)

    embeddings_pairs: list[tuple[Embedding, Embedding]] = []
    for embs in temp_to_embeddings.values():
        embeddings_pairs.extend(combinations(embs, 2))

    assert len(embeddings_pairs) == sum(
        len(v) * (len(v) - 1) // 2 for v in temp_to_embeddings.values()
    )
    return embeddings_pairs


async def calculate_similarities_and_save(args: Namespace):
    with open(args.input_file, "r") as f:
        samples = [Sample.model_validate_json(line) for line in f]
        assert len(samples) > 1, "Need at least 2 samples to calculate similarities"

    embeddings = await generate_embeddings(args.embedding_model, samples)
    embeddings_pairs = pair_embeddings(samples, embeddings)
    similarities = [
        cosine_similarity(emb1, emb2)
        for emb1, emb2 in tqdm(embeddings_pairs, desc="Similarities")
    ]

    with open(args.output_file, "w") as f:
        for similarity in similarities:
            f.write(similarity.model_dump_json() + "\n")
