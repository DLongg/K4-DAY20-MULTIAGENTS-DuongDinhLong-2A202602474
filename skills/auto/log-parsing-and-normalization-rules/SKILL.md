---
name: log-parsing-and-normalization-rules
description: Use when parsing log files, extracting error entries, and formatting JSON outputs.
---
# Log Parsing and Normalization Rules

- **Service Name Formatting:** Normalize service names in output schemas according to rules (e.g., convert lower-case strings with hyphens to underscores, such as `payment-service` to `payment_service`).
- **Sorting Multilevel Collections:** Ensure output lists (such as error entries) are sorted deterministically by primary keys and timestamps in ascending order (e.g., sorted by service name, then by UTC timestamp).
- **Required Top-Level Fields:** Include all mandatory metadata and schema version keys (e.g., `"schema_version"` and `"generated_by"`) in top-level JSON output objects.