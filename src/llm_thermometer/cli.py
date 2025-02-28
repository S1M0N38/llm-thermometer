"""Command-line interface for llm-thermometer."""

import argparse
import asyncio
import sys
from argparse import Namespace
from datetime import datetime
from pathlib import Path

from llm_thermometer import generate, measure

TEMPERATURES = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def cmd_generate(args: Namespace):
    """Generate samples and save them into <data_dir>/samples"""

    (args.data_dir / "samples").mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    args.output_file = args.data_dir / "samples" / f"{timestamp}.jsonl"

    if args.temperature:
        args.temperature = float(args.temperature)
        asyncio.run(generate.generate_samples_and_save(args))
    else:
        for temperature in TEMPERATURES:
            args.temperature = temperature
            asyncio.run(generate.generate_samples_and_save(args))


def cmd_measure(args: Namespace):
    """Calculate similarities for all samples in <data_dir>/samples
    and save them into <data_dir>/similarities"""

    (args.data_dir / "similarities").mkdir(exist_ok=True)
    for input_file in (args.data_dir / "samples").glob("*.jsonl"):
        output_file = input_file.parent.parent / "similarities" / input_file.name
        if not output_file.exists():
            args.input_file = input_file
            args.output_file = output_file
            asyncio.run(measure.calculate_similarities_and_save(args))


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="LLM Thermometer - Estimate temperature values of LLMs"
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # Generate command
    generate_parser = subparsers.add_parser(
        name="generate",
        help="Generate multiple LLM samples",
    )
    generate_parser.add_argument(
        "--language-model",
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
        "--data-dir",
        type=Path,
        required=True,
        help="Directory to save generated samples",
    )
    generate_parser.add_argument(
        "--temperature",
        type=str,
        default="",
        help="Temperature to use in samples generation",
    )

    # Measure command
    measure_parser = subparsers.add_parser(
        name="measure",
        help="Measure semantic similarity of samples",
    )
    measure_parser.add_argument(
        "--embedding-model",
        type=str,
        required=True,
        help="Embedding model for computing embeddings",
    )
    measure_parser.add_argument(
        "--data-dir",
        type=Path,
        required=True,
        help="Directory with samples to measure",
    )

    args = parser.parse_args()

    assert args.data_dir.is_dir() and args.data_dir.exists()

    match args.command:
        case "generate":
            cmd_generate(args)

        case "measure":
            cmd_measure(args)

        case _:
            parser.print_help()
            sys.exit(1)


if __name__ == "__main__":
    main()
