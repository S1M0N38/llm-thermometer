## v0.3.1 (2025-03-01)

### Fix

- **measure**: compute embs pairs within the temp group

## v0.3.0 (2025-02-28)

### Feat

- **cli**: update cli for file creation based on session
- **makefile**: update recipes to new CLI interface
- **makefile**: add generate-all and measure-all recipes

### Fix

- **measure**: close httpx client
- **generate**: close the httpx client

### Refactor

- **measure**: merge compute sim to compute and save sim

## v0.2.0 (2025-02-28)

### Feat

- **makefile**: add recipe for measuring similarities
- **measure**: add script for computing semantic similarities
- **cli**: add measure command to CLI
- **models**: update fields for Similarity model
- **models**: add Embedding model
- **models**: move models to models.py and add id to Sample

### Fix

- **generate**: reduce max tokens to 400
- **generate**: limit the generation to 500 toks

## v0.1.0 (2025-02-27)

### Feat

- **makefile**: add makefile with simple generation recipe
- **cli**: move CLI into a separate module
- **pyproject**: add build system and cli interface
- **generate**: initial version of generate.py script
- initial project src
