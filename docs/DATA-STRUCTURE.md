# DATA-STRUCTURE.md — SkillCorner ACB 2025/2026 · Dataset Schema & Relationship Map

> **Phase 1 — Data Discovery** (per `AGENT.md` lifecycle).
> This document profiles every file, its schema, cardinality, key mappings, missingness notes, and join patterns.
> Never paste raw data into prompts — always run profiling scripts and embed summarised outputs here.

---

## 1. Repository Layout

```
data/
├── matches.json                             # Structured list of the 10 sample games
├── player_id_aliases.csv                    # Canonical player ID mapping (9 players, 2 IDs each)
├── aggregates/
│   ├── acb_shotsaggregates_20252026.csv     # 326 rows / 316 distinct players
│   ├── acb_drivesaggregates_20252026.csv    # 301 rows
│   └── acb_picksaggregates_20252026.csv     # 319 rows
└── matches/
    └── {gameId}/                            # 10 folders, one per game
        ├── {gameId}_game_data.json          # Metadata + rosters
        ├── {gameId}_dynamic_events.json     # All event tables (20 keys) for one game
        └── {gameId}_tracking_data.jsonl.gz  # 25 fps XY tracking (~30–46 MB/game, LFS)
```

### Sample Games

| gameId | Date | Home | Away | Score |
|---|---|---|---|---|
| 114243 | 2025-10-11 | BAXI Manresa | Coviran Granada | 83-68 |
| 114234 | 2025-10-18 | Casademont Zaragoza | Leche Rio Breogan | 84-88 |
| 114169 | 2025-12-14 | CB UCAM Murcia | Club Joventut Badalona | 80-77 |
| 114099 | 2026-01-31 | Basquet Girona | San Pablo Burgos | 77-71 |
| 114086 | 2026-02-08 | Dreamland Gran Canaria | Bitci Baskonia | 75-97 |
| 178442 | 2026-03-21 | BC MoraBanc Andorra | Bilbao Basket | 98-102 |
| 179612 | 2026-04-12 | Malaga | Valencia BC | 89-96 |
| 184439 | 2026-04-19 | Real Madrid | Lenovo Tenerife | 90-95 |
| 188630 | 2026-05-03 | BC Barcelona | Dreamland Gran Canaria | 91-69 |
| 191313 | 2026-05-29 | Leche Rio Breogan | Casademont Zaragoza | 94-95 |

---

## 2. Data Layers Overview

| Layer | Files | Grain | Size | Coverage |
|---|---|---|---|---|
| **Tracking** | `{gameId}_tracking_data.jsonl.gz` | Frame (25 fps) — player + ball XY/Z in feet | ~30–46 MB/game | 10 games |
| **Dynamic Events** | `{gameId}_dynamic_events.json` | Per event: touch, shot, pick, drive, … | ~5–15 MB/game | 10 games |
| **Season Aggregates** | `data/aggregates/*.csv` | Per player-team-season, offense-only | 3 CSVs | 293 games |
| **Game Metadata** | `{gameId}_game_data.json` | Per game (rosters + context) | small | 10 games |

> **Critical:** Aggregates cover 293 games; raw events cover only 10. These 10 events are a strict subset — season totals cannot be reproduced from them.

---

## 3. File Schemas & Field Summaries

### 3.1 `matches.json`

Flat list of the 10 sample games. Key fields:

| Field | Type | Notes |
|---|---|---|
| `gameId` | INT | Primary key; names the `matches/{gameId}/` folder |
| `date_time` | STRING | Official ACB tip-off UTC; matches `date` in `game_data.json` |
| `competition_id` | INT | League identifier |
| `competition_edition_id` | INT | Edition identifier |
| `season_id` | INT | Season identifier |
| `home_team` / `away_team` | OBJECT | `id`, `name` |
| `home_score` / `away_score` | INT | Final score |

---

### 3.2 `player_id_aliases.csv`

9 players have 2 `player_id` values across the season. **Always apply before any player-level join.**

| Field | Type | Notes |
|---|---|---|
| `player_id` | INT | An alias player ID found in some games |
| `canonical_player_id` | INT | The canonical ID to merge on |

```python
# Pattern: apply before any join
aliases = pl.read_csv("data/player_id_aliases.csv")
df = df.join(aliases, on="player_id", how="left")
df = df.with_columns(
    pl.coalesce(["canonical_player_id", "player_id"]).alias("player_id")
).drop("canonical_player_id")
```

---

### 3.3 `{gameId}_game_data.json`

Game context + rosters. One file per game.

| Field | Type | Notes |
|---|---|---|
| `gameId` | INT | Primary key |
| `date` | STRING | Game date |
| `competition`, `season` | OBJECT | Identifiers and names |
| `homeTeam` / `awayTeam` | OBJECT | `id`, `name`, `players[]` |
| `players[].playerId` | INT | Joins to all event-table player ID fields |
| `players[].name`, `.position` | STRING | Display name and position |

---

### 3.4 `{gameId}_tracking_data.jsonl.gz`

One JSON line per video frame at 25 fps. **Do not read entire file into memory — stream or sample.**

| Field | Type | Notes |
|---|---|---|
| `frameIdx` | INT | Frame count since video start; joins to `frame`/`startFrame`/`endFrame` on event tables |
| `wallClock` | INT | Milliseconds since video start; same origin as event `wallClock` |
| `gameClock` | FLOAT | Seconds remaining in period |
| `period` | INT | Period number (1-indexed) |
| `shotClock` | FLOAT | Seconds remaining on shot clock |
| `players` | LIST[OBJECT] | One entry per tracked player |
| `players[].playerId` | INT | Joins to `game_data` player IDs |
| `players[].xyz` | LIST[FLOAT] | `[x, y, z]` in feet; `z=0` for players, positive for ball |
| `players[].speed` | FLOAT | Speed in feet/second |
| `players[].isDetected` | BOOL | `true` = directly detected; `false` = extrapolated |
| `players[].predError` | FLOAT | Predicted position error in feet (extrapolated positions only) |
| `ball` | OBJECT | `xyz`, `isDetected` |

> **Tracking quality:** ~76–83% directly detected. Extrapolated positions average ~4.4–5.2 ft error. Apply smoothing (Kalman filter or Savitzky-Golay) before computing velocities or accelerations.

```python
# Read tracking without decompressing:
import pandas as pd
df_tracking = pd.read_json(
    "data/matches/114243/114243_tracking_data.jsonl.gz",
    lines=True, compression="gzip"
)
```

---

### 3.5 `{gameId}_dynamic_events.json` — 20 Event Tables

One JSON file per game containing a dict with 20 keys. Each key maps to a list of event records.

```python
import json, pathlib
events = json.loads(
    pathlib.Path("data/matches/114243/114243_dynamic_events.json").read_bytes()
)
# Keys: possessions, chances, chance_players, matchups,
#       shots, free_throws, rebounds, turnovers, fouls, timeouts,
#       passes, touches, dribbles,
#       picks, handoffs, off_ball_screens, drives, isolations, posts, closeouts
```

#### Common Fields (shared by most/all event tables)

| Field | Type | Notes |
|---|---|---|
| `id` | STRING | Unique event ID within its table |
| `gameId` | INT | Joins to `game_data` |
| `season` | STRING | Season label |
| `period` | INT | Period number (1 = first quarter) |
| `chanceId` | STRING | Parent chance; joins to `chances` |
| `possessionId` | STRING | Parent possession; joins to `possessions` |
| `startFrame` / `endFrame` | INT | Tracking frame range at 25 fps |
| `startWallClock` / `endWallClock` | INT | Ms since video start |
| `startGameClock` / `endGameClock` | FLOAT | Seconds remaining in period |

---

## 4. Entity Relationship Diagram

```
game_data (per game)
    │
    ├── [gameId] ──────────────────────────────────────────────────────┐
    │                                                                   │
tracking_data (frames @ 25fps)                                         │
    │ frameIdx ←→ startFrame / endFrame / frame (events)               │
    │ wallClock ←→ startWallClock / endWallClock (events)              │
    │                                                                   │
possessions                                                            │
    │ possessionId ─────────────────────────────────────────────────┐  │
    │                                                               │  │
    └── chances                                                     │  │
            │ chanceId ──────────────────────────────────────────┐  │  │
            │ offPlayerIds / defPlayerIds (lineup arrays)        │  │  │
            │                                                    │  │  │
            ├── chance_players [per player per chance]           │  │  │
            │       matchupId → matchups                         │  │  │
            │                                                    │  │  │
            ├── [Outcome Events]  ←─────────────── chanceId ────┘  │  │
            │     shots          ← touchId → touches                │  │
            │     free_throws                                        │  │
            │     rebounds                                           │  │
            │     turnovers                                          │  │
            │     fouls                                              │  │
            │     timeouts                                           │  │
            │                                                        │  │
            ├── [Ball-Movement Events]  ←─────── chanceId ──────┐   │  │
            │     passes         ← touchId → touches             │   │  │
            │     touches        (central connective tissue)     │   │  │
            │     dribbles       ← touchId → touches             │   │  │
            │                                                    │   │  │
            └── [Action Markings]  ←──────────── chanceId ──────┘   │  │
                  picks           ← touchId → touches               │  │
                  handoffs        ← touchId → touches               │  │
                  off_ball_screens                                   │  │
                  drives          ← touchId → touches               │  │
                  isolations      ← touchId → touches               │  │
                  posts           ← touchId → touches               │  │
                  closeouts                                          │  │
                                                                     │  │
aggregates/ (293 games) ── player_id → player_id_aliases ───────────┘  │
    acb_shotsaggregates                                                  │
    acb_drivesaggregates                                                 │
    acb_picksaggregates                                                  │
        └── [player_id, team_id, season_id] → game_data.players ────────┘
```

---

## 5. Join Key Reference

| Join | From | To | Key |
|---|---|---|---|
| Any event → game metadata | All tables | `game_data` | `gameId` |
| Any event → parent chance | All event tables | `chances` | `chanceId` |
| Any event → parent possession | All event tables | `possessions` | `possessionId` |
| Touch-linked event → touch context | `shots`, `picks`, `drives`, `passes`, `handoffs`, `isolations`, `posts`, `dribbles` | `touches` | `touchId` |
| Tracking frame → event | `tracking_data` | any event table | `frameIdx` ↔ `startFrame`/`endFrame` |
| Tracking wall time → event | `tracking_data` | any event table | `wallClock` ↔ `startWallClock` |
| On-court presence → player | `chance_players` | `game_data` players | `playerId` |
| Defensive assignment | `matchups` | `chance_players` | `matchupId` |
| Player deduplication | all tables | `player_id_aliases.csv` | `player_id` → `canonical_player_id` |
| Aggregate → event-level | `aggregates/*.csv` | any event table | `player_id`, `team_id`, `season_id` |

---

## 6. Event Table Schemas (Key Fields)

### 6.1 `possessions`

| Field | Type | Description |
|---|---|---|
| `id` | STRING | Possession ID |
| `offTeamId` | INT | Offensive team |
| `startType` | STRING | How possession started (e.g. `jump_ball`, `inbound`, `defensive_rebound`) |
| `startFrame` / `endFrame` | INT | Tracking frames |
| `duration` | FLOAT | Possession duration in seconds |

### 6.2 `chances`

The **central unit** of play-by-play. Almost every other event hangs off a `chanceId`.

| Field | Type | Description |
|---|---|---|
| `id` | STRING | Chance ID |
| `possessionId` | STRING | Parent possession |
| `offTeamId` / `defTeamId` | INT | Offensive and defensive team |
| `offPlayerIds` | LIST[INT] | On-court offensive lineup |
| `defPlayerIds` | LIST[INT] | On-court defensive lineup |
| `startType` | STRING | How chance started (e.g. `off_rebound`, `def_rebound`, `turnover`) |
| `outcome` | STRING | Chance outcome (e.g. `made_basket`, `missed_shot`, `turnover`) |
| `ptsScored` | INT | Points scored — **do not use for team totals** (see KNOWN_ISSUES) |
| `qualityIndex` | FLOAT | Tracking confidence (0–1); filter on `usable=true` for reliable spatial metrics |
| `usable` | BOOL | Whether tracking quality is sufficient for spatial analysis |

### 6.3 `touches`

The **connective tissue** linking ball movement to action markings.

| Field | Type | Description |
|---|---|---|
| `id` | STRING | Touch ID (referenced as `touchId` in picks, drives, shots, etc.) |
| `playerId` | INT | Ball handler |
| `defenderId` | INT | Assigned matchup defender (or nearest if no rotation) |
| `dribbleCount` | INT | Dribbles taken during this touch |
| `duration` | FLOAT | Touch duration in seconds |
| `startLoc` / `endLoc` | LIST[FLOAT] | Player position at start/end in feet |
| `closestDefLoc` / `endClosestDefLoc` | LIST[FLOAT] | Defender position at start/end |

### 6.4 `shots`

| Field | Type | Description |
|---|---|---|
| `shooterId` | INT | Shooter |
| `location` | LIST[FLOAT] | XY at release in feet |
| `region` | STRING | Court zone (e.g. `ra`, `left wing three`) |
| `three` | BOOL | 3-point attempt |
| `outcome` | BOOL | Made (true) / missed |
| `fouled` | BOOL | Fouled on attempt (excluded from FIBA `attempts` count) |
| `assisted` | BOOL | Assisted |
| `distance` | FLOAT | Shooter-to-hoop distance at release in feet |
| `contestLevel` | STRING | `open`, `light`, `average`, `plus`, `blocked` |
| `closestDefDist` | FLOAT | Distance to closest defender at release in feet |
| `closestDefId` | INT | Closest defender |
| `complexShotType` | STRING | `catchAndShoot`, `dribblePullUp`, `layup`, `dunk`, `stepback`, … |
| `releaseTime` | FLOAT | Seconds from touch start to release |
| `shotQuality` | FLOAT | SkillCorner 0–100 quality score |
| `touchId` | STRING | Touch during which shot was taken |

### 6.5 `picks`

| Field | Type | Description |
|---|---|---|
| `ballhandlerId` / `screenerId` | INT | The two actors |
| `ballhandlerDefId` / `screenerDefId` | INT | Their respective defenders (tracking-derived) |
| `bhrDefType` | STRING | Ball-handler defensive coverage: `blitz`, `ice`, `over`, `switch`, `under` |
| `scrDefType` | STRING | Screener defensive coverage: `blitz`, `ice`, `show`, `soft`, `switch` |
| `location` | LIST[FLOAT] | Pick location in feet |
| `locationType` | STRING | `middle`, `stepUp`, `wing`, `unknown` |
| `direct` | BOOL | **Must be `true` for aggregate comparisons** (~52% of rows) |
| `touchId` | STRING | Ball-handler's touch during the pick |

### 6.6 `drives`

| Field | Type | Description |
|---|---|---|
| `playerId` | INT | Driver |
| `category` | STRING | How drive was created: `pick`, `handoff`, `iso`, `closeout`, `off_ball_screen`, `miscellaneous` |
| `endType` | STRING | How drive ended: `kickout`, `pullout`, `pullup`, `interior_pass`, `shot_near_basket`, `turnover`, `stoppage` |
| `direction` | STRING | `left`, `right` |
| `blowby` | BOOL | Defender beaten |
| `dribbleThrough` | BOOL | Driver went through the paint |
| `touchId` | STRING | Touch during the drive |

### 6.7 `closeouts`

| Field | Type | Description |
|---|---|---|
| `closingOutPlayerId` | INT | Closing defender |
| `ballHandlerId` | INT | Ball handler being closed out |
| `startDistance` / `touchDistance` / `endDistance` | FLOAT | Defender-to-ball-handler distance at 3 checkpoints |
| `startLoc` / `touchLoc` / `endLoc` | LIST[FLOAT] | Defender location at 3 checkpoints |
| `touchWallClock` | **STRING** | ⚠️ **Cast to INT before arithmetic** (type quirk in ACB 2025-2026) |

### 6.8 `chance_players`

| Field | Type | Description |
|---|---|---|
| `playerId` | INT | Player on court |
| `chanceId` | STRING | The chance they participated in |
| `offTeamId` | INT | Player's team role in this chance |
| `startMatchupId` / `endMatchupId` | STRING | Defensive assignment at start/end |
| `shotLoc` / `rimLoc` / `reboundLoc` | LIST[FLOAT] | Player position at 3 key moments |
| `minutesPlayed` | FLOAT | On-court time in this chance |

### 6.9 `matchups`

| Field | Type | Description |
|---|---|---|
| `id` | STRING | Matchup ID (referenced in `chance_players`) |
| `offPlayerId` | INT | Offensive player |
| `defPlayerId` | INT | Defensive player guarding them |
| `startFrame` / `endFrame` | INT | Duration of this assignment |

### 6.10 `passes`

| Field | Type | Description |
|---|---|---|
| `passerId` | INT | Passer |
| `receiverId` | INT | Receiver |
| `toReceiverId` | INT | ⚠️ **Holds intercepting defender, NOT intended receiver** (see KNOWN_ISSUES) |
| `passerLoc` / `receiverLoc` | LIST[FLOAT] | XY locations in feet |
| `passerRegion` / `receiverRegion` | STRING | Court zones |
| `touchId` | STRING | Touch of the passer |

---

## 7. Season Aggregate Schemas

All three CSVs share the same identity columns. Metric families are documented in [`docs/aggregates_columns.md`](aggregates_columns.md).

### 7.1 Identity Columns (all three files)

| Column | Type | Notes |
|---|---|---|
| `competition_id` / `competition_name` | INT / STRING | ACB competition |
| `season_id` / `season_name` | INT / STRING | 2025-2026 |
| `player_id` / `player_name` | INT / STRING | Join via `player_id_aliases.csv` first |
| `team_id` / `team_name` | INT / STRING | NULL `team_id` = season total for traded player |
| `games_played` | INT | On-court presence in SkillCorner's 293-game set |
| `possessions_played` | INT | Offensive possessions on court |

### 7.2 Grain & Double-Count Warning

```python
# NEVER aggregate both per-team and total rows for the same player.
# Filter examples (Polars):
per_team_only   = df.filter(pl.col("team_id").is_not_null())
season_totals   = df.filter(pl.col("team_name") == "total")
```

### 7.3 Shots Aggregate — Metric Families

| Family | Columns | Notes |
|---|---|---|
| **Totals** | `attempts`, `made_baskets`, `total_points`, `assisted_mades`, `avg_attempts_distance`, … | `attempts` excludes fouled misses (FIBA convention) |
| **By contest level** (`cl_*`) | 5 buckets × 7 metrics = 35 cols | `open`, `light`, `average`, `plus`, `blocked` |
| **By court zone** (`zone_*`) | 71 cols | `restricted_area`, `paint_non_ra`, `mid_range`, `corner_3`, `wing_3_*`, `top_3`, … |
| **By shot type** (`cst_*`) | 14 types × 7 metrics = 98 cols | `catch_and_shoot`, `dribble_pull_up`, `dunk`, `layup`, `stepback`, … |
| **Catch-and-shoot / off-dribble** (`cns_*` / `od_*`) | 30 cols | Coarse 2-way split |
| **Contested / uncontested** | 30 cols | Coarse 2-way split |

### 7.4 Drives Aggregate — Metric Families

| Family | Columns | Notes |
|---|---|---|
| **Totals** | `total_drives`, `successful_drives`, `made_baskets`, `assists`, `fouls`, … | |
| **By category** (`category_*`) | 6 types × 2 cols | `pick`, `handoff`, `iso`, `closeout`, `off_ball_screen`, `miscellaneous` |
| **By end type** (`end_type_*`) | 7 types × 2 cols | `kickout`, `pullout`, `pullup`, `interior_pass`, `shot_near_basket`, `turnover`, `stoppage` |
| **By direction** | 4 cols | `left` / `right` count + rate |
| **Drive quality** | `blowby_*`, `dribble_through_*`, `direct_drives_*` | Tracking-derived quality signals |

### 7.5 Picks Aggregate — Metric Families

| Family | Columns | Notes |
|---|---|---|
| **Role totals** | `handler_*` / `screener_*` — 35 cols per role | Points, assists, pass decisions, fouls, ppp … |
| **By defensive coverage** | `handler_*_vs_{blitz,ice,over,switch,under}` / `screener_*_vs_{blitz,ice,show,soft,switch}` | ~245 cols per role |
| **By screen location** | `*_at_{middle,stepUp,wing,unknown}` — 36 cols per role | |
| **Always-null** | `handler_fg2_pct_vs_blitz`, `handler_ppp_at_unknown`, `handler_score_rate_at_unknown`, `screener_ppp_at_unknown`, `screener_score_rate_at_unknown` | Zero events in ACB 25-26, not missing data |

> **Direct picks only:** Filter `direct = true` before comparing raw event counts to aggregates (~52% of raw pick events).

---

## 8. Coordinate System Reference

```
         Positive Y (left when attacking)
              │
 Offensive    │                    Defensive
   Hoop  ─────┼─────────────────────  Hoop
 (neg x)      │                    (pos x)
              │
         Negative Y (right when attacking)

Origin (0, 0): Center court
Units: feet
Ball Z: positive = above ground; Player Z: always 0
Speed: feet/second
```

### Region Vocabulary

```
"left corner three"   "left corner two"    "left wing three"   "left wing two"
"middle three"        "middle two"          "key"               "ra" (restricted area)
"right wing three"    "right wing two"      "right corner three" "right corner two"
"backcourt"           "far"
```

---

## 9. Timing Conventions

| Clock | Use When | Units |
|---|---|---|
| `wallClock` / `frame` / `frameIdx` | Aligning events with tracking frames | ms / frame index |
| `gameClock` + `period` | In-game analysis, ignoring dead time | seconds remaining in period |
| `shotClock` | Shot clock pressure analysis | seconds remaining |

> `wallClock` runs through dead time; `gameClock` stops on whistles.
> Approximate: `frameIdx ≈ wallClock_ms ÷ 40`.

---

## 10. Key Cardinalities (ACB 2025-2026)

| Entity | Count | Source |
|---|---|---|
| Games (full season) | 327 | ACB official |
| Games (in aggregates) | 293 | SkillCorner delivery |
| Games (raw tracking/events) | 10 | This dataset |
| Teams | 18 | ACB 2025-2026 |
| Distinct players (shots agg) | 316 | `acb_shotsaggregates_20252026.csv` |
| Total pick events (full season) | 42,156 | `picks` tables |
| Direct picks (for aggregates) | 22,080 (~52%) | `picks` where `direct=true` |
| Shot events (FIBA `attempts`) | 38,029 | Season aggregates |
| Total shot events (incl. fouled misses) | 41,684 | Raw `shots` tables |
| Tracking fps | 25 | Fixed |

---

## 11. Profiling Scripts

> Run these locally and paste only the summarised output. Never embed raw data.

### 11.1 Schema Profiler

```python
# scripts/profile_dynamic_events.py
import json, sys, pathlib

game_id = sys.argv[1]
path = pathlib.Path(f"data/matches/{game_id}/{game_id}_dynamic_events.json")
events = json.loads(path.read_bytes())

for key, rows in events.items():
    if rows:
        fields = list(rows[0].keys())
        print(f"\n{key}: {len(rows)} rows")
        print(f"  Fields ({len(fields)}): {', '.join(fields[:10])}{'...' if len(fields) > 10 else ''}")
    else:
        print(f"\n{key}: 0 rows (empty)")
```

### 11.2 Tracking Frame Sampler

```python
# scripts/sample_tracking.py
import pandas as pd, sys

game_id = sys.argv[1]
path = f"data/matches/{game_id}/{game_id}_tracking_data.jsonl.gz"
df = pd.read_json(path, lines=True, compression="gzip", nrows=100)
print(f"Columns: {list(df.columns)}")
print(f"Frame range: {df['frameIdx'].min()} – {df['frameIdx'].max()}")
print(f"Players per frame: {df['players'].apply(len).describe()}")
```

### 11.3 Aggregate Missingness Check

```python
# scripts/check_aggregates_missingness.py
import polars as pl

for fname in [
    "data/aggregates/acb_shotsaggregates_20252026.csv",
    "data/aggregates/acb_drivesaggregates_20252026.csv",
    "data/aggregates/acb_picksaggregates_20252026.csv",
]:
    df = pl.read_csv(fname)
    null_counts = df.null_count()
    high_null = [(col, null_counts[col][0]) for col in df.columns if null_counts[col][0] > 0]
    print(f"\n{fname}: {df.shape[0]} rows x {df.shape[1]} cols")
    print(f"  High-null columns: {high_null[:5]}{'...' if len(high_null) > 5 else ''}")
```

---

## 12. Known Data Issues (Summary)

Full details: [`docs/KNOWN_ISSUES.md`](KNOWN_ISSUES.md).

| Issue | Impact | Fix |
|---|---|---|
| 9 players with dual `player_id` | Double rows in aggregates | Apply `player_id_aliases.csv` before any join |
| `chances.ptsScored` mislabelled in ~50% of games | Wrong team score totals | Compute from `shots` + `free_throws` |
| `passes.toReceiverId` = intercepting defender | Incorrect if used as intended receiver | Use as defender ID only |
| `shots` includes fouled misses not in FIBA `attempts` | Raw count > aggregate `attempts` | Filter `fouled = false` for box-score FGA |
| Picks aggregates = direct only (~52% of events) | Raw event count ~2× aggregate total | Filter `direct = true` before comparing |
| `closeouts.touchWallClock` is STRING | Arithmetic fails | Cast to INT: `int(row["touchWallClock"])` |
| Tracking extrapolation: ~17–24% of positions | Noisy speeds/accelerations | Apply smoothing before kinematic metrics |
| `games_played` reflects 293-game delivery | Not comparable to official FIBA appearances | Document caveat in all player-level reports |