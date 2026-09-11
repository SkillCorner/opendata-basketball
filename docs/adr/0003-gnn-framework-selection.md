# ADR 0003 — GNN Framework Selection for Space Creation Index (SCI)

**Date:** 2026-09-10
**Status:** Accepted
**Deciders:** Project team
**Layer:** `infrastructure` / `use_cases/sci`

---

## Context

The Space Creation Index (SCI) requires converting per-frame tracking snapshots into graphs where:
- **Nodes** = players (10 per frame) with features [x, y, speed, team, has_ball, defender_dist, is_detected]
- **Edges** = spatial relationships (distance, is_guarding, same_team)
- **Labels** = per-possession offensive efficiency (whether the team scored)

A GNN message-passing architecture learns which spatial configurations generate scoring opportunities.
This drives the per-player, per-frame space ownership computation.

---

## Decision

**Use `unravelsports` v1.2.0** as the GNN framework wrapper, with **PyTorch Geometric** as the backend.

`unravelsports` provides:
- Tracking data -> graph conversion with Polars DataFrames as input
- Configurable node/edge feature definitions
- Pre-built GNN architectures (GCN, GAT, GraphSAGE)
- Native support for multi-frame sequence labeling

### Architecture Chosen

```
Graph per possession-chance (aggregated from all frames in chance):
  Node features per player: [rel_x, rel_y, speed, is_offense, has_ball, dist_to_basket, def_dist]
  Edge features per pair:   [euclidean_dist, is_guarding, same_team]
  Graph label:              chance_outcome (1 = scored, 0 = did not score)

Model: GraphSAGE (2 layers, hidden_dim=64)
  -> per-node embedding -> mean pool -> binary classification head
  -> SHAP values on node embeddings -> per-player SCI contribution
```

---

## Alternatives Considered

| Alternative | Reason Not Chosen |
|---|---|
| **PyTorch Geometric raw** | More flexible but requires building graph conversion from scratch |
| **DGL (Deep Graph Library)** | Less active community; no SkillCorner-specific utilities |
| **NetworkX + sklearn** | No deep learning; insufficient for learning spatial patterns |
| **Spektral (TensorFlow)** | Python 3.11 only; project uses Python 3.12 |

---

## Tradeoffs

| Factor | Benefit | Risk / Mitigation |
|---|---|---|
| unravelsports abstraction | 70-80% boilerplate reduction | Version lock; pin to 1.2.0 in requirements |
| GraphSAGE | Fast, inductive (works on unseen lineups) | Less expressive than attention models; acceptable for sample size |
| Per-chance aggregation | Aligns with chance as analysis unit | Loses frame-level temporal structure; documented as limitation |
| 10-game sample | Feasible training | Overfitting risk; mitigated by k-fold CV on chance level |

---

## Consequences

- `infrastructure/graph_builder.py`: wraps `unravelsports.GraphConverter` for SkillCorner data format
- `use_cases/sci/gnn_model.py`: GraphSAGE training loop + SHAP explainability
- `use_cases/sci/sci_calculator.py`: converts node-level SHAP values to per-player SCI scores
- GNN model artifacts (weights) stored in `models/` (gitignored)
- See ADR 0005 for SCI validation strategy
