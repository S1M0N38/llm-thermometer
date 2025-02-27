"""Module for generating multiple responses from LLMs to estimate temperature."""

import argparse
import asyncio
import logging
import os
from argparse import Namespace
from pathlib import Path

from openai import AsyncOpenAI
from pydantic import BaseModel
from tqdm.asyncio import tqdm

CONCURRENT_REQUESTS = 32  # NOTE: larger values could cause stalling issues

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

assert (LLM_API_KEY := os.getenv("LLM_API_KEY", ""))
assert (LLM_BASE_URL := os.getenv("LLM_BASE_URL", ""))


class Sample(BaseModel):
    model: str
    prompt: str
    completion: str
    temperature: float | None = None


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
    )

    completion = response.choices[0].message.content
    assert completion

    return Sample(
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
    assert len(args.prompts) > 0, "Prompt cannot be empty"
    assert not args.output_file.exists(), "Output file must not exist"
    assert args.output_file.suffix == ".jsonl", "Output file must be a JSONL file"
    assert args.samples > 0, "Samples must be greater than 0"

    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
    client = AsyncOpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

    async def generate_with_semaphore():
        async with semaphore:
            return await generate_sample_and_save(
                client=client,
                model=args.model,
                prompt=args.prompt,
                temperature=args.temperature,
                output_file=args.output_file,
            )

    tasks = [generate_with_semaphore() for _ in range(args.samples)]
    desc = f"{args.model} - {args.temperature}"
    for _ in tqdm.as_completed(tasks, total=len(tasks), desc=desc):
        pass


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate multiple LLM samples",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model to use for the LLM",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Prompt to send to the LLM",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=32,
        help="Number of samples to generate",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        required=True,
        help="Output file path (JSONL)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Temperature to use",
    )

    args = parser.parse_args()
    await generate_samples_and_save(args)


if __name__ == "__main__":
    asyncio.run(main())
