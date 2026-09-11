# ADR 0004 — Data Pipeline Architecture

**Date:** 2026-09-10
**Status:** Accepted
**Deciders:** Project team
**Layer:** All layers

---

## Context

The project requires two independent but coordinated pipelines:
1. **BAV Pipeline**: Event-driven, processes `touches`/`shots`/`picks`/`drives`/`passes` per game
2. **SCI Pipeline**: Tracking-driven, processes 25fps frame arrays per chance

Both pipelines must be fully reproducible from raw files, share player identity resolution,
output JSON contracts for the presentation layer, and complete locally without cloud infrastructure.

---

## Decision

**Adopt a linear, phase-gated pipeline** with clear input/output contracts per stage:

```
Phase 1 - Ingestion (infrastructure/)
  raw JSON/JSONL.gz -> typed Polars DataFrames + XY arrays
  Output: normalized event tables, tracking frame arrays

Phase 2 - Feature Engineering (use_cases/bav/ + use_cases/sci/)
  BAV: action sequences per chance + spatial state features
  SCI: per-chance spatial graphs (PyTorch Geometric objects)
  Output: feature matrices + graph datasets

Phase 3 - Modeling (use_cases/bav/ + use_cases/sci/)
  BAV: XGBoost training -> SHAP-based action values
  SCI: GraphSAGE training -> node SHAP -> SCI scores
  Output: per-action BAV scores, per-player SCI scores (10 games)

Phase 4 - Aggregation + Validation (use_cases/player_value/)
  BAV + SCI combined -> Full Spectrum Player Value
  Validate vs. season aggregates (external benchmarks)
  Output: player_value_rankings.json

Phase 5 - Presentation (presentation/)
  JSON -> standalone HTML5 report
  Output: reports/full_spectrum_player_value.html
```

### Key Design Rules
- Each phase reads from well-defined input files; never skips phases
- All randomness uses `RANDOM_SEED = 42` (set in `domain/constants.py`)
- No phase writes to a previous phase's output directory

---

## Alternatives Considered

| Alternative | Reason Not Chosen |
|---|---|
| **Airflow / Prefect DAG** | Overkill for 10-game dataset; adds setup complexity |
| **Jupyter notebooks only** | Not reproducible as clean pipeline; violates Clean Architecture |
| **Single monolithic script** | Untestable; no layer separation |

---

## Tradeoffs

| Factor | Benefit | Risk / Mitigation |
|---|---|---|
| Linear phases | Simple mental model; easy to checkpoint | Less parallelism; acceptable for this scale |
| Polars throughout | Consistent API; fast for medium data | Steeper learning curve; documented in AGENT.md |
| Phase-gate checkpoints | Easy to resume from any phase | Requires saving intermediate artifacts as parquet |

---

## Consequences

- Intermediate outputs in `outputs/` (gitignored): `outputs/events/`, `outputs/features/`, `outputs/scores/`
- All pipeline entrypoints are CLI commands in `presentation/cli.py`
- `pyproject.toml` defines all dependencies with pinned versions
