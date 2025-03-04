# Contributing

Welcome to the LLM Thermometer project! This tool helps estimate the temperature parameter of Large Language Models through semantic similarity analysis. We appreciate your interest in contributing to this project and are excited to see your ideas and improvements.

This guide will help you set up your development environment, understand the project structure, and follow our contribution workflow. Whether you're fixing bugs, adding features, or improving documentation, this guide should have you covered.

## Environment Setup

This section describes how to set up the **recommended** development environment for this project [uv](https://docs.astral.sh/uv/).

1. Download the repository:

```sh
git clone https://github.com/S1M0N38/llm-thermometer.git
cd llm-thermometer
```

2. Create environment:

```sh
uv venv
uv sync --dev
```

3. Set up environment variables:

```sh
cp .envrc.example .envrc
# And modify the .envrc file
```

The environment setup is now ready to use. Every time you are working on the project, you can activate the environment by running:

```sh
source .envrc
```

> You can use [direnv](https://github.com/direnv/direnv) to automatically activate the environment when you enter the project directory.

## Project Structure

The LLM Thermometer project follows a structured organization to facilitate development and maintenance:

```
llm-thermometer/
├── src/llm_thermometer/       # Main Python package
│   ├── __init__.py            # Version information
│   ├── cli.py                 # Command-line interface
│   ├── generate.py            # LLM response generation
│   ├── measure.py             # Semantic similarity measurement
│   ├── models.py              # Pydantic data models
│   ├── report.py              # Report generation
│   └── templates/             # Jinja2 templates
│       ├── index.md.jinja     # Index page template
│       └── report.md.jinja    # Report template
│
├── docs/                      # Generated documentation
│   ├── index.md               # Documentation index
│   ├── reports/               # Generated experiment reports
│   └── assets/                # Report visualizations and images
│       └── [experiment_id]/   # Assets organized by experiment ID
│
├── data/                      # Data directory (gitignored)
│   ├── samples/               # Generated LLM samples
│   └── similarities/          # Computed similarities
│
├── .github/                   # GitHub configuration
│   └── workflows/             # GitHub Actions workflows
│
├── docker-compose.yml         # Docker configuration for local models
├── Makefile                   # Automation for common tasks
├── pyproject.toml             # Project metadata and dependencies
├── README.md                  # Project overview
├── CHANGELOG.md               # Version history
├── CITATION.cff               # Citation information
├── CONTRIBUTING.md            # Contribution guidelines
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── .gitignore                 # Git ignore patterns
├── .gitattributes             # Git attributes (LFS configuration)
└── .python-version            # Python version specifier
```

### Core Modules

- **generate.py**: Handles the generation of LLM responses with different temperature values.
- **measure.py**: Computes semantic similarities between generated responses using embedding models.
- **report.py**: Processes the data and produces reports with visualizations and statistics.
- **models.py**: Defines the data structures used throughout the project.
- **cli.py**: Implements the command-line interface for the tool.

### Data Flow

1. **Generation**: `generate.py` produces samples from an LLM saved to `data/samples/`
2. **Measurement**: `measure.py` computes similarities between samples saved to `data/similarities/`
3. **Reporting**: `report.py` generates reports from the data saved to `docs/reports/`

## Project Style Guide

The project style guide is enforced using [pre-commit](https://pre-commit.com/).

To install pre-commit hooks, run:

```sh
pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
```

The following hooks are used:

- [conventional-commits](https://www.conventionalcommits.org/en/v1.0.0/): for consistent commit messages.
- [ruff](https://docs.astral.sh/ruff/) for linting and formatting.
- [uv](https://docs.astral.sh/uv/) for managing environment and dependencies.

## Version Release

> Release tags are only created manually by the repository owner.

Release tags are based on [semantic versioning](https://semver.org/). The release process makes use of [commitizen](https://commitizen-tools.github.io/commitizen/).

The following steps are used to produce a new release:

1. Bump the version number and generate CHANGELOG.md by locally running `cz bump`
2. Push the generated commit and tag to origin with `git push --follow-tags`
