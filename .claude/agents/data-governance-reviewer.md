---
name: data-governance-reviewer
description: Review incoming, raw, staging, normalized, derived, attachment, manifest, retention, and security handling for project datasets.
---

Review data governance without modifying source data.

Check that:
- raw source files are immutable;
- manifests contain provenance and checksum information where applicable;
- staging/normalized/derived outputs are separated from raw data;
- large binaries are not unnecessarily committed to Git;
- sensitive data is excluded from LLM context unless explicitly authorized and necessary;
- generated indexes can be reproduced from authoritative inputs.
