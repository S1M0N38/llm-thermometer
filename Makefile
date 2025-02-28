LANGUAGE_MODEL := unsloth/Mistral-Small-24B-Instruct-2501-bnb-4bit
EMBEDDING_MODEL := intfloat/multilingual-e5-large
PROMPT := "What will technology look like in 2050?"
SAMPLES := 32
TEMPERATURE := 0.7
DATA_DIR := data
TEMPS := 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0

################################################################################
# Generation and measurement for temperature = 0.7

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

################################################################################
# Generation and measurement for various temperatures

generate-temp-%:
	llm-thermometer generate \
		--model $(LANGUAGE_MODEL) \
		--prompt $(PROMPT) \
		--samples $(SAMPLES) \
		--temperature $* \
		--output-file $(DATA_DIR)/samples_temp_$*.jsonl

measure-temp-%:
	llm-thermometer measure \
		--model $(EMBEDDING_MODEL) \
		--input-file $(DATA_DIR)/samples_temp_$*.jsonl \
		--output-file $(DATA_DIR)/samples_temp_$*.similarities.jsonl

# Generate all temperature variants
generate-all:
	$(foreach temp,$(TEMPS),$(MAKE) generate-temp-$(temp);)

# Measure all temperature variants
measure-all:
	$(foreach temp,$(TEMPS),$(MAKE) measure-temp-$(temp);)
