---
name: register-artifact
description: Register a new project document, dataset, attachment, requirement, feature, interface, API, test case, defect, change request, or decision in the correct repository location with consistent metadata and relationships.
---

# Register Artifact

1. Search for an existing matching artifact or ID first.
2. Classify the item as Wiki knowledge, entity, dataset/raw data, attachment, AI draft, or generated output.
3. Use an existing template from `templates/` when available.
4. Assign a stable ID only when the artifact type requires one.
5. Preserve source/provenance and related entity IDs.
6. For raw data, create/update `data/manifests/`; never alter the source file in place.
7. For AI-created drafts, write to `llm/generated/` until approved.
8. Run structure validation after repository changes.
