# ADR 0002 — Spatial Engine Selection for Tracking Data Processing

**Date:** 2026-09-10
**Status:** Accepted
**Deciders:** Project team
**Layer:** infrastructure

---

## Context

The SkillCorner tracking data is delivered as JSONL.gz files (~30-46 MB/game) at 25 fps.
Each frame contains 10+ player XY/Z positions, speeds, and detection flags.
To compute the SCI/GNN model and BAV spatial features, we need efficient:
1. Decompression and frame-level iteration
2. XY array extraction and manipulation
3. Velocity, acceleration, and distance computation
4. Alignment of tracking frames with event wallClock timestamps

Two candidate approaches were considered.

---

## Decision

**Use loodlight as the primary tracking ingestion layer**, specifically loodlight.io.skillcorner
(a native SkillCorner adapter), combined with **Polars** for all downstream tabular operations.

For spatial graph construction (SCI/GNN), use **unravelsports** which natively accepts
Polars DataFrames and converts them to PyTorch Geometric graphs.

### Stack

`
JSONL.gz -> floodlight.io.skillcorner -> floodlight.core.XY (numpy arrays)
    -> custom infrastructure adapter -> Polars DataFrame
    -> unravelsports GraphConverter -> PyTorch Geometric Data objects
`

---

## Alternatives Considered

| Alternative | Reason Not Chosen |
|---|---|
| **Raw pandas.read_json** | Works but no structured XY model; no SkillCorner-specific handling |
| **Custom JSONL parser from scratch** | Reinvents floodlight wheel; more maintenance burden |
| **numpy only** | No SkillCorner IO adapter; harder to integrate with unravelsports |

---

## Tradeoffs

| Factor | Benefit | Risk / Mitigation |
|---|---|---|
| floodlight dependency | Proven SkillCorner adapter, clean XY abstraction | Adds dependency; mitigated by pinned version |
| Polars for tabular ops | Faster than pandas for large frames; native unravelsports support | Different API from pandas; documented in AGENT.md |
| unravelsports for GNN | Reduces GNN boilerplate significantly | Version-sensitive; pin to 1.2.0 |

---

## Consequences

- infrastructure/tracking_loader.py wraps floodlight SkillCorner IO
- infrastructure/graph_builder.py wraps unravelsports GraphConverter
- All tracking XY arrays stored as Polars DataFrames in the pipeline
- Frame rate (25fps) and coordinate system (feet, center-court origin) documented in domain types
