# 🌡️ LLM Thermometer

Estimate temperature values of Large Language Models (LLMs) through semantic similarity analysis of generated text.

## Research Question

Is it possible to infer the temperature parameter value used by an LLM from only the generated text? Probably [yes](https://s1m0n38.github.io/llm-thermometer/reports/20250303T144808.html).

## Approach

LLM Thermometer uses semantic similarity between multiple responses to estimate temperature:

1. **Generation**: Produce multiple responses from an LLM using the same prompt
2. **Similarity Analysis**: Measure semantic similarity between responses
3. **Temperature Estimation**: Infer temperature based on response diversity
   - Higher temperature → More diverse responses (lower similarity)
   - Lower temperature → More consistent responses (higher similarity)

The reports, hosted on [GitHub Pages](https://s1m0n38.github.io/llm-thermometer/), contains experiments metadata, charts, and tables.

## Usage

```bash
# Set required environment variables
export LLM_API_KEY="your_api_key"
export LLM_BASE_URL="https://api.provider.com/v1"
export EMB_API_KEY="your_embedding_api_key"
export EMB_BASE_URL="https://api.provider.com/v1"
```

```bash
# Generate samples
llm-thermometer generate \
 --language-model "model-name" \
 --prompt "What will technology look like in 2050?" \
 --samples 32 \
 --data-dir ./data \
 --temperature 0.7 \

# Measure semantic similarity
llm-thermometer measure \
 --embedding-model "embedding-model-name" \
 --data-dir ./data

# Generate report
llm-thermometer report \
 --data-dir ./data \
 --docs-dir ./docs

# Or using Makefile...
make generate
make measure
make report
make docs
```

## Installation

The preferred way to install `llm-thermometer` is using [`uv`](https://docs.astral.sh/uv/) (although you can also use `pip`).

```bash
# Clone the repository
git clone https://github.com/S1M0N38/llm-thermometer.git
cd llm-thermometer

# Create a virtual environment
uv init

# Install the package
uv sync
```

## Models Local Deployment with Docker

If you have a GPU available, you can run both the Language Model and embedding model locally using docker-compose:

```bash
# Set HF_HOME environment variable for model caching
export HF_HOME="/path/to/huggingface/cache"

# Start the models
docker-compose up -d

# Language model will be available at http://localhost:41408
# Embedding model will be available at http://localhost:41409
```

## Requirements

- Python 3.12+
- OpenAI-compatible API endpoints (`/chat/completions` and `/embeddings`)
- NVIDIA GPU (for local deployment with docker-compose)
