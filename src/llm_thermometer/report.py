"""Module for generating reports from data"""

import logging
from argparse import Namespace

from jinja2 import Environment, PackageLoader, select_autoescape

from llm_thermometer.models import Sample, Similarity

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)


def generate_report_and_save(args: Namespace):
    with open(args.samples_file, "r") as f:
        samples = [Sample.model_validate_json(line) for line in f]
    with open(args.similarities_file, "r") as f:
        similarities = [Similarity.model_validate_json(line) for line in f]

    env = Environment(
        loader=PackageLoader("llm_thermometer"),
        autoescape=select_autoescape(),
    )
    template = env.get_template("report.html.jinja")
    ...
