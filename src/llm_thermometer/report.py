"""Module for generating reports from data"""

import logging
from argparse import Namespace
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from jinja2 import Environment, PackageLoader, select_autoescape
from matplotlib.figure import Figure

from llm_thermometer import __version__
from llm_thermometer.models import Experiment, Sample, Similarity

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

env = Environment(
    loader=PackageLoader("llm_thermometer"),
    autoescape=select_autoescape(),
)


plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Helvetica", "Arial", "sans-serif"],
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "axes.grid": True,
        "grid.alpha": 0.5,
        "grid.linestyle": ":",
        "figure.dpi": 300,
        "savefig.dpi": 300,
    }
)

plt.style.use("seaborn-v0_8-whitegrid")


def violinplot(df, figsize=(10, 5), ylim=(-0.2, 1.2), save_path=None) -> Figure:
    fig, ax = plt.subplots(figsize=figsize)

    sns.violinplot(
        x="temperature",
        y="similarity",
        hue="temperature",
        data=df,
        palette="coolwarm",
        legend=False,
        inner="quartile",
        ax=ax,
    )

    ax.set_ylim(ylim)
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Similarity")
    ax.grid(axis="y", linestyle=":", alpha=0.8)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    plt.tight_layout(pad=2)
    if save_path is not None:
        plt.savefig(save_path, bbox_inches="tight")

    return fig


def generate_plots_and_save(df: pd.DataFrame, save_dir: Path):
    violinplot(df, save_path=save_dir / "violinplot.png")


def files_to_experiment(samples_file: Path, similarities_file: Path) -> Experiment:
    with open(samples_file, "r") as f:
        samples = [Sample.model_validate_json(line) for line in f]
        sample = samples[0]
        assert all(sample.model == s.model for s in samples)
        assert all(sample.prompt == s.prompt for s in samples)

    with open(similarities_file, "r") as f:
        similarities = [Similarity.model_validate_json(line) for line in f]
        similarity = similarities[0]
        assert all(similarity.model == s.model for s in similarities)

    assert samples_file.stem == similarities_file.stem

    return Experiment(
        id=samples_file.stem,
        language_model=sample.model,
        embedding_model=similarity.model,
        prompt=sample.prompt,
    )


def generate_report_and_save(args: Namespace):
    with open(args.samples_file, "r") as f:
        df_samples = pd.DataFrame.from_records(
            [Sample.model_validate_json(line).model_dump() for line in f]
        )

    with open(args.similarities_file, "r") as f:
        df_similarities = pd.DataFrame.from_records(
            [Similarity.model_validate_json(line).model_dump() for line in f],
        )

    df = df_similarities.merge(
        df_samples[["id", "temperature"]],
        left_on="sample_id1",
        right_on="id",
    ).drop(columns=["id"])

    experiment = files_to_experiment(args.samples_file, args.similarities_file)

    template = env.get_template("report.md.jinja")
    md_content = template.render(
        experiment=experiment,
        version=__version__,
        tables={},
        plots={},
    )

    with open(args.output_file, "w") as f:
        f.write(md_content)
        logging.info(f"Report saved to {args.output_file}")

    generate_plots_and_save(df, args.docs_dir / "reports" / experiment.id)
    logging.info(f"Plots saved to {args.docs_dir / 'reports' / experiment.id}")


def generate_index_and_save(args):
    experiments = [
        files_to_experiment(
            args.data_dir / "samples" / path.with_suffix(".jsonl").name,
            args.data_dir / "similarities" / path.with_suffix(".jsonl").name,
        )
        for path in (args.docs_dir / "reports").rglob("*.md")
    ]

    # sort by prompt, langauge model, emebdding model and id
    experiments = sorted(
        experiments, key=lambda e: (e.prompt, e.language_model, e.embedding_model, e.id)
    )

    template = env.get_template("index.md.jinja")
    output_file = args.docs_dir / "index.md"
    md_content = template.render(experiments=experiments, version=__version__)

    with open(output_file, "w") as f:
        f.write(md_content)

    logging.info(f"Docs index saved to {output_file}")
