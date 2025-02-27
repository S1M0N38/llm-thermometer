MODEL := unsloth/Mistral-Small-24B-Instruct-2501-bnb-4bit
PROMPT := "What will technology look like in 2050?"
SAMPLES := 32
TEMPERATURE := 0.7
OUTPUT_DIR := data

generate:
	llm-thermometer generate \
		--model $(MODEL) \
		--prompt $(PROMPT) \
		--samples $(SAMPLES) \
		--temperature $(TEMPERATURE) \
		--output-file $(OUTPUT_DIR)/generate-test.jsonl
