all: generate measure report

LANGUAGE_MODEL := unsloth/Mistral-Small-24B-Instruct-2501-bnb-4bit
EMBEDDING_MODEL := jinaai/jina-embeddings-v2-base-en
PROMPT := "What will technology look like in 2050?"
SAMPLES := 32
MAX_TOKENS := 2048
DATA_DIR := data
DOCS_DIR := docs
TEMPERATURE := ""
EXP_ID := ""

generate:
	@echo "Generating samples..."
	@echo "Prompt: $(PROMPT)"
	@echo "Language Model: $(LANGUAGE_MODEL)"
	@echo "Samples: $(SAMPLES)"
	@llm-thermometer generate \
		--language-model $(LANGUAGE_MODEL) \
		--prompt $(PROMPT) \
		--samples $(SAMPLES) \
		--max_tokens $(MAX_TOKENS) \
		--data-dir $(DATA_DIR) \
		--temperature $(TEMPERATURE)

measure:
	@llm-thermometer measure \
		--embedding-model $(EMBEDDING_MODEL) \
		--data-dir $(DATA_DIR)

report:
	@llm-thermometer report \
		--data-dir $(DATA_DIR) \
		--docs-dir $(DOCS_DIR) \
		--exp-id $(EXP_ID)

docs:
	@llm-thermometer report \
		--data-dir $(DATA_DIR) \
		--docs-dir $(DOCS_DIR) \
		--index

.PHONY: all generate measure report docs
