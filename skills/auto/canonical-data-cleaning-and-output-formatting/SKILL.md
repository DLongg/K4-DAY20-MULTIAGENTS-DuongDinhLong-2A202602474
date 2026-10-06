---
name: canonical-data-cleaning-and-output-formatting
description: Use when processing datasets, cleaning CSVs, and generating JSON answers or summary metrics.
---
# Canonical Data Cleaning and Output Formatting

- **Financial Values in Cents:** When required by schema rules, express all money values as integer cents (e.g., multiply decimal or float currency amounts by 100 and cast to integer).
- **Metadata Blocks:** Ensure JSON output files contain required metadata objects (e.g., `meta` containing keys like `source`, `rows_in`, and `rows_used`) tracking raw and filtered row counts.
- **Canonical Schemas:** Strictly adhere to specified headers, column ordering, date formats (e.g., ISO-8601 UTC strings), and categorical spelling conventions when writing clean data files (e.g., `workspace/clean.csv`).