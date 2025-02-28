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
