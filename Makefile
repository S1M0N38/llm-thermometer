LANGUAGE_MODEL := unsloth/Mistral-Small-24B-Instruct-2501-bnb-4bit
EMBEDDING_MODEL := intfloat/multilingual-e5-large
PROMPT := "What will technology look like in 2050?"
SAMPLES := 32
DATA_DIR := data
TEMPERATURE := ""

generate:
	@llm-thermometer generate \
		--language-model $(LANGUAGE_MODEL) \
		--prompt $(PROMPT) \
		--samples $(SAMPLES) \
		--data-dir $(DATA_DIR) \
		--temperature $(TEMPERATURE)

measure:
	@llm-thermometer measure \
		--embedding-model $(EMBEDDING_MODEL) \
		--data-dir $(DATA_DIR)
