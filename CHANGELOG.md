## v0.5.2 (2025-03-04)

### Fix

- **templates**: remove linear regression from reports

## v0.5.1 (2025-03-04)

### Fix

- **templates**: add new lines after report tables

## v0.5.0 (2025-03-03)

### Feat

- increase ctx window for language model
- **templates**: add scatter plot avg/std to report tempalte
- **models**: add samples to Experiment model
- add exp_id to CLI for selecting specific report
- add max-tokens to CLI
- **report**: add scatter plot avg/std
- **templates**: update report template with plots and stats
- **report**: add basic plots and stats
- **docs**: auto generate reports
- **report**: add violin plot to report
- **templates**: update templates to support new report format

### Fix

- **templates**: group reports by prompt
- **report**: group reports by prompts in index
- remove center div in markdown report
- update link to reports in index.md
- **docs**: auto generated docs with new dir structure
- save images in docs/assets subdirs
- **report**: update index generation to docs subdir structure
- **tempaltes**: update footer link

## v0.4.0 (2025-03-01)

### Feat

- **report**: add index gen and utils function
- **templates**: update preamble of the report template
- **makefile**: add docs recipe for docs/index generation
- **templates**: add index.md.jinja
- **models**: add Experiment model
- **cli**: add --index flag for docs generation
- **templates**: replace html template with markdown template
- **report**: add report module
- **templates**: add empty report template
- **cli**: add report subcommand
- **makefile**: add report and all recipes

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
