"""Module for generating multiple responses from LLMs to estimate temperature."""

import asyncio
import logging
import os
from argparse import Namespace
from pathlib import Path

from openai import AsyncOpenAI
from tqdm import tqdm

from llm_thermometer.models import Sample

MAX_TOKENS = 400  # NOTE: this limitation is imposed by the embedding model
CONCURRENT_REQUESTS = 32  # NOTE: larger values could cause stalling issues

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

assert (LLM_API_KEY := os.getenv("LLM_API_KEY", ""))
assert (LLM_BASE_URL := os.getenv("LLM_BASE_URL", ""))


async def generate_sample(
    client: AsyncOpenAI,
    model: str,
    prompt: str,
    temperature: float | None,
) -> Sample:
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=MAX_TOKENS,
    )

    completion = response.choices[0].message.content
    assert completion

    return Sample(
        id=response.id,
        model=model,
        prompt=prompt,
        completion=completion,
        temperature=temperature,
    )


async def generate_sample_and_save(
    client: AsyncOpenAI,
    model: str,
    prompt: str,
    temperature: float | None,
    output_file: Path,
):
    sample = await generate_sample(
        client=client,
        model=model,
        prompt=prompt,
        temperature=temperature,
    )

    with open(output_file, "a") as f:
        f.write(sample.model_dump_json() + "\n")


async def generate_samples_and_save(args: Namespace):
    assert len(args.prompt) > 0, "Prompt cannot be empty"
    assert args.samples > 0, "Samples must be greater than 0"
    assert 0 <= args.temperature <= 1, "0 <= temperature <= 1"

    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
    client = AsyncOpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

    async def generate_with_semaphore():
        async with semaphore:
            return await generate_sample_and_save(
                client=client,
                model=args.language_model,
                prompt=args.prompt,
                temperature=args.temperature,
                output_file=args.output_file,
            )

    tasks = [generate_with_semaphore() for _ in range(args.samples)]
    for future in tqdm(
        asyncio.as_completed(tasks),
        total=len(tasks),
        desc=f"{args.language_model} - temp: {args.temperature}",
    ):
        await future
