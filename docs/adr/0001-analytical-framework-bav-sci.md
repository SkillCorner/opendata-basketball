# ADR 0001 — Analytical Framework Selection: BAV + SCI (GNN)

**Date:** 2026-09-10
**Status:** Accepted
**Deciders:** Project team
**Layer:** `use_cases` / `domain`

---

## Context

The SkillCorner Basketball Analytics Cup evaluates submissions on five equal pillars: Relevance, Methodology, Originality, Communication, and Open-Source Potential. The dataset is uniquely rich — 25 fps broadcast tracking for all 10 players + ball, combined with 20 named event tables from Game Intelligence — enabling analyses that are impossible with traditional play-by-play feeds.

Two core questions drive this project:

1. **What is the value of each on-ball action?** Every touch, pass, pick, drive and shot changes the probability of scoring. Quantifying this delta — per action, per player — is the foundation of **Basketball Action Value (BAV)**.
2. **What is the value of a player who never touches the ball?** Off-ball positioning, movement, and court spacing directly create or destroy scoring opportunities. Quantifying this from 25 fps tracking is the foundation of the **Space Creation Index (SCI)**, powered by a Graph Neural Network.

Together, BAV and SCI answer the full player value question: **"What is the total contribution of a player — on ball and off ball?"**

---

## Decision

**Adopt BAV + SCI as a single unified analytical framework** under the project name:

> **"Full Spectrum Player Value: Quantifying On-Ball and Off-Ball Contributions in ACB Basketball via Action Value Models and Graph Neural Networks"**

The two components are mathematically complementary:
- BAV captures value from **actions that happen** (on-ball events with outcomes)
- SCI captures value from **positioning and movement** (off-ball tracking state)
- Combined player value = `BAV_season + SCI_season` (normalized per possession)

### Scope

| Component | Inputs | Output |
|---|---|---|
| **BAV model** | `touches`, `passes`, `shots`, `picks`, `drives`, `chances`, `tracking_data` | Per-action value score (probability delta) |
| **SCI/GNN model** | `tracking_data`, `matchups`, `chance_players`, `off_ball_screens` | Per-frame space ownership -> per-possession SCI |
| **Unified score** | BAV + SCI (per possession normalized) | Season player ranking: Full Spectrum Player Value |

---

## Design Alternatives Within BAV + SCI

| Design Question | Chosen Approach | Alternative Discarded |
|---|---|---|
| BAV model type | XGBoost with SHAP (fast, explainable) | LSTM/Transformer sequence model (higher complexity, harder to explain) |
| BAV action space | Custom taxonomy from SkillCorner event tables | SPADL format (soccer-native, requires adaptation with higher loss of basketball context) |
| SCI model type | GraphSAGE — inductive, works on unseen lineups | GCN — transductive, cannot generalize beyond training graph structure |
| SCI granularity | Per-chance aggregation aligned with `chanceId` | Per-frame individual scores (too noisy for model supervision at 10-game scale) |
| Score combination | Simple average BAV + SCI (transparent) | Learned weighting via meta-model (opaque, overfits to small sample) |

---

## Tradeoffs

| Factor | Benefit | Risk / Mitigation |
|---|---|---|
| Combined scope | Maximum criteria coverage | Higher complexity; mitigated by strict phase gating (AGENT.md) |
| GNN component | Novel and original | Requires PyTorch; mitigated by using `unravelsports` library |
| VAEP methodology | Academically grounded | Soccer-native; mitigated by custom basketball action taxonomy |
| 10-game sample | Sufficient for proof-of-concept | Not season-level; mitigated by using aggregates as external benchmarks |

---

## Consequences

- All `use_cases/` modules structured around two sub-domains: `bav/` and `sci/`
- A unified `PlayerValue` domain entity aggregates both scores
- Presentation layer produces: (1) BAV leaderboard, (2) SCI leaderboard, (3) combined ranking
- Validation: BAV vs. season aggregate PPP; SCI vs. team offensive rating
- See ADR 0003 for GNN framework selection and ADR 0005 for validation strategy
