# ADR 0005 — Validation Strategy

**Date:** 2026-09-10
**Status:** Accepted
**Deciders:** Project team
**Layer:** `use_cases`

---

## Context

The project operates on two data scopes:
- **10-game raw events + tracking**: used for model training and per-game BAV/SCI computation
- **293-game season aggregates**: used as external validation benchmarks only

The primary data leakage risk is using season aggregate statistics as features inside
a model trained on the 10-game subset.

---

## Decision

### BAV Validation Protocol

```
Training split: 8 games (stratified by team)
Test split: 2 games (held out by game -- prevent game-level leakage)

Metric: Brier score (probability calibration)
Baseline: Constant predictor at mean chance success rate
Secondary: Spearman rank correlation, per-player BAV vs. season aggregate PPP (expected rho > 0.5)

Leakage rule: Season aggregate columns MUST NOT appear as features.
```

### SCI Validation Protocol

```
Training split: 8 games (k-fold CV on chance level within games)
Test split: 2 games

Metric: AUC-ROC (chance scored classification)
Baseline: Logistic regression on shot distance alone
Secondary: Spearman rho, per-player SCI vs. team offensive rating (expected > 0.4)

Leakage assertion (automated test):
  assert no feature column name appears in aggregate CSV column list
```

### Combined Validation

```
Full Spectrum Player Value = (BAV_normalized + SCI_normalized) / 2
Rank correlation vs. season aggregate points_per_shot and PPP (expected rho > 0.45)
Face validity: Top 5 players match known ACB star players
```

---

## Tradeoffs

| Factor | Benefit | Risk / Mitigation |
|---|---|---|
| Game-level holdout | Prevents game-level leakage | Only 2 test games; wide CIs; documented |
| Spearman rank correlation | Non-parametric; robust to outliers | Correlation not causation; documented as validation not proof |
| Leakage assertion in tests | Automated guard rail | Only checks column names; manual semantic review required |

---

## Consequences

- `tests/use_cases/test_leakage.py` contains automated leakage assertion
- `RANDOM_SEED = 42` used in all model training calls
- Train/test game split in `PLAN.md` with specific gameIds
- Validation results embedded in final HTML report
