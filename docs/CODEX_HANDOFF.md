# CODEX_HANDOFF

Updated: 2026-10-07
Trigger phrase: **"chạy với codex"**

## Current snapshot
- Default branch: `main`
- Latest observed commit: `bbff173bae0e40f6c8164d2bb42233f63e7f5797`
- Commit: build: regenerate STEP library [skip ci]
- Read `docs/PROJECT_CONTEXT.md` before creating or modifying models.

## Codex execution contract
On **"chạy với codex"**, inspect branch/status/history and project context first, preserve verified models and local changes, use a feature branch, implement/generate only the requested models, run the project's generation/validation steps, re-import STEP outputs and verify bounding boxes. Write `.ai/AI_REPORT.md`, commit/push for Web review. Never auto-merge `main`, force-push, or bulk-regenerate unrelated assets.

## Guardrails
- PCB-critical dimensions take priority over cosmetic proportions.
- Do not scale an entire model to hide footprint/model mismatch.
- PCB plane is Z=0; THT solder tails go below Z=0; SMD feet sit on Z=0.
