"""Command-line interface for llm-thermometer."""

import argparse
import asyncio
import sys
from pathlib import Path

from llm_thermometer import generate, measure


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="LLM Thermometer - Estimate temperature values of LLMs"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate command
    generate_parser = subparsers.add_parser(
        "generate", help="Generate multiple LLM samples"
    )
    generate_parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model to use for the LLM",
    )
    generate_parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Prompt to send to the LLM",
    )
    generate_parser.add_argument(
        "--samples",
        type=int,
        default=32,
        help="Number of samples to generate",
    )
    generate_parser.add_argument(
        "--output-file",
        type=Path,
        required=True,
        help="Output file path (JSONL)",
    )
    generate_parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Temperature to use",
    )

    # Generate command
    measure_parser = subparsers.add_parser(
        "measure", help="Measure semantic similarity of samples"
    )
    measure_parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Embedding model for computing embeddings",
    )
    measure_parser.add_argument(
        "--input-file",
        type=Path,
        required=True,
        help="Input file path with samples (JSONL)",
    )
    measure_parser.add_argument(
        "--output-file",
        type=Path,
        required=True,
        help="Output file path with computed measures (JSONL)",
    )

    args = parser.parse_args()

    if args.command == "generate":
        asyncio.run(generate.generate_samples_and_save(args))
    elif args.command == "measure":
        asyncio.run(measure.calculate_similarities_and_save(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
