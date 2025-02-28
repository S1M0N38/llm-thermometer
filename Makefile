LANGUAGE_MODEL := unsloth/Mistral-Small-24B-Instruct-2501-bnb-4bit
EMBEDDING_MODEL := intfloat/multilingual-e5-large
PROMPT := "What will technology look like in 2050?"
SAMPLES := 32
TEMPERATURE := 0.7
DATA_DIR := data

generate:
	llm-thermometer generate \
		--model $(LANGUAGE_MODEL) \
		--prompt $(PROMPT) \
		--samples $(SAMPLES) \
		--temperature $(TEMPERATURE) \
		--output-file $(DATA_DIR)/samples.jsonl

measure:
	llm-thermometer measure \
		--model $(EMBEDDING_MODEL) \
		--input-file $(DATA_DIR)/samples.jsonl \
		--output-file $(DATA_DIR)/samples.similarities.jsonl
