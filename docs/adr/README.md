# Architecture Decision Records (ADRs)

This directory contains the Architecture Decision Records for the Full Spectrum Player Value project.
Each ADR documents a significant design decision: its context, the chosen approach, alternatives considered, and consequences.

## Format

Each ADR follows the MADR (Markdown Architectural Decision Records) format:
- **Status**: Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
- **Context**: Why was this decision needed?
- **Decision**: What was chosen?
- **Alternatives Considered**: What else was evaluated?
- **Tradeoffs**: Benefits and risks
- **Consequences**: What changes as a result?

## Index

| ADR | Title | Status | Layer |
|---|---|---|---|
| [0001](0001-analytical-framework-bav-sci.md) | Analytical Framework: BAV + SCI (GNN) | Accepted | use_cases, domain |
| [0002](0002-spatial-engine-selection.md) | Spatial Engine: floodlight + unravelsports | Accepted | infrastructure |
| [0003](0003-gnn-framework-selection.md) | GNN Framework: GraphSAGE via unravelsports | Accepted | infrastructure, use_cases/sci |
| [0004](0004-data-pipeline-architecture.md) | Data Pipeline Architecture (5 phases) | Accepted | All layers |
| [0005](0005-validation-strategy.md) | Validation Strategy (BAV + SCI + Combined) | Accepted | use_cases |

## Adding a New ADR

1. Copy the template below
2. Name the file XXXX-short-title.md (next sequential number)
3. Fill in all sections
4. Add to the index table above
5. Reference the ADR from TASK.md in the relevant task

### Template

`markdown
# ADR XXXX — Title

**Date:** YYYY-MM-DD
**Status:** Proposed
**Deciders:** Project team
**Layer:** [domain | use_cases | infrastructure | presentation | all]

---

## Context
[Why is this decision needed?]

## Decision
[What was decided?]

## Alternatives Considered
| Alternative | Reason Not Chosen |
|---|---|
| ... | ... |

## Tradeoffs
| Factor | Benefit | Risk / Mitigation |
|---|---|---|
| ... | ... | ... |

## Consequences
[What changes as a result of this decision?]
`
