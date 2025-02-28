# LLM Thermometer

Estimate temperature values of Large Language Models (LLMs) through semantic similarity analysis of generated text.

## Research Question

Is it possible to infer the temperature parameter value used by an LLM when generating text without direct access to that parameter?

## Approach

LLM Thermometer uses semantic similarity between multiple responses to estimate temperature:

1. **Generation**: Produce multiple responses from an LLM using the same prompt
2. **Similarity Analysis**: Measure semantic similarity between responses
3. **Temperature Estimation**: Infer temperature based on response diversity
   - Higher temperature → More diverse responses (lower similarity)
   - Lower temperature → More consistent responses (higher similarity)

## Usage

```bash
# Set required environment variables
export LLM_API_KEY="your_api_key"
export LLM_BASE_URL="https://api.provider.com/v1"
export EMB_API_KEY="your_embedding_api_key"
export EMB_BASE_URL="https://api.provider.com/v1"

# Generate samples
llm-thermometer generate \
  --model "model-name" \
  --prompt "What will technology look like in 2050?" \
  --samples 32 \
  --temperature 0.7 \
  --output-file data/samples.jsonl

# Measure semantic similarity
llm-thermometer measure \
  --model "embedding-model-name" \
  --input-file data/samples.jsonl \
  --output-file data/samples.similarities.jsonl

# Or use the Makefile
make generate
make measure
```

## Installation

```bash
# Clone the repository
git clone https://github.com/S1M0N38/llm-thermometer.git
cd llm-thermometer

# Install the package
pip install -e .
```

## Local Deployment with Docker

If you have a GPU available, you can run both the Language Model and embedding model locally using docker-compose:

```bash
# Set HF_HOME environment variable for model caching
export HF_HOME="/path/to/huggingface/cache"

# Start the models
docker-compose up -d

# LLM will be available at http://localhost:41408
# Embedding model will be available at http://localhost:41409
```

## Requirements

- Python 3.12+
- OpenAI-compatible API endpoint
- NVIDIA GPU (for local deployment with docker-compose)
