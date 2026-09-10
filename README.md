# SkillCorner Open Data — Basketball

## About this repo

### Description

This repo contains broadcast tracking data collected by [SkillCorner](https://skillcorner.com) for 10 games of the Spanish Liga ACB 2025-2026 season, the derived Dynamic Events (Game Intelligence) for those same games, and season-level offensive aggregates (shots, drives, picks) for 293 ACB 2025-2026 games.

Broadcast tracking data is tracking data collected through computer vision and machine learning out of the broadcast video, with no on-court hardware and no dependency on a venue's own camera system.

### Motivation

This data is open sourced to:
* Provide access to basketball tracking data to researchers and the sports analytics community.
* Increase awareness of broadcast tracking data and how it can benefit clubs, media and the betting industry.
* Allow SkillCorner prospects to access data easily, parse our data format and get started building on top of it.
* Offer two entry points: full-season aggregates for quick analysis, and raw tracking plus events for those who want to build from the ground up.

If you use the data, we kindly ask that you credit SkillCorner and notify us on [Twitter](https://twitter.com/skillcorner) so we can follow the work being done with it.

## Documentation

Start with the [primer](docs/PRIMER.md) for an overview of what this data is, the coordinate system, units, frame rate and clock conventions, and how the aggregates are computed. Field-by-field reference for every table lives in [`docs/data_dictionary/`](docs/data_dictionary/README.md); the aggregate CSV columns are documented separately in [`docs/aggregates_columns.md`](docs/aggregates_columns.md).

There are no tutorial notebooks in this repo — the primer and data dictionary are written to be read directly by both analysts and LLMs; most people will get further asking an LLM to work with the data using these docs as context than following a fixed notebook.

### Data Structure

The `data` directory contains:

* `aggregates/` — three CSVs with season-level, offense-only aggregated Dynamic Events for 293 of the 327 games of ACB 2025-2026 (regular season and playoffs); the missing games are mostly the playoffs plus a few regular-season fixtures:
  * `acb_shotsaggregates_20252026.csv`
  * `acb_drivesaggregates_20252026.csv`
  * `acb_picksaggregates_20252026.csv`
  * See [`docs/aggregates_columns.md`](docs/aggregates_columns.md) for the full column reference.
* `player_id_aliases.csv` — maps the few duplicate `player_id` values to one canonical id per player (see [Known data issues](#known-data-issues)).
* `matches/` — one folder per game (named with its `gameId`), for the 10 sample games. Each folder has exactly three files:
  * `{gameId}_game_data.json` — game metadata and both team rosters. See [`docs/data_dictionary/game_data.md`](docs/data_dictionary/game_data.md).
  * `{gameId}_dynamic_events.json` — a single JSON object with one array per event family (chances, possessions, shots, picks, drives, passes, touches, dribbles, free_throws, fouls, rebounds, turnovers, timeouts, isolations, handoffs, posts, off_ball_screens, closeouts, chance_players, matchups — see the exact key names in [`docs/data_dictionary/README.md`](docs/data_dictionary/README.md)). Every record carries `id`, `gameId`, `season`, `period` and the `chanceId`/`possessionId` it belongs to, so the file is a relational bundle you can load and join in one pass.
  * `{gameId}_tracking_data.jsonl.gz` — gzip-compressed JSON Lines, one video frame per line at 25 fps (player and ball positions). Roughly 30-46 MB per game. Tracked with Git LFS. Decompress with `gzip -d {gameId}_tracking_data.jsonl.gz`, or read directly without decompressing first: `pandas.read_json("{gameId}_tracking_data.jsonl.gz", lines=True, compression="gzip")`. See [`docs/data_dictionary/tracking_data.md`](docs/data_dictionary/tracking_data.md) for the frame schema.

The 10 sample games (ACB 2025-2026):

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

See `data/matches.json` for the same list as structured data (team ids, `competition_id`/`competition_edition_id`/`season_id`, final scores). Its `date_time` is the official ACB scheduled tip-off in UTC, and matches the `date` field inside each `{gameId}_game_data.json`; tracking may start slightly before or after that instant.

### 📍 Tracking Data

Player and ball positions at 25 frames per second, in feet, origin at the center of the court. See [`docs/data_dictionary/tracking_data.md`](docs/data_dictionary/tracking_data.md) for the full field list and [`docs/PRIMER.md`](docs/PRIMER.md#coordinate-system-and-units) for the coordinate system.

### ⚡ Dynamic Events (Game Intelligence)

Every touch, pass, dribble, shot, foul, rebound, turnover, timeout, and named action (pick-and-roll, hand-off, off-ball screen, drive, isolation, post-up, closeout) SkillCorner's Game Intelligence models detect from the tracking data, each carrying both play-by-play facts (who, what, outcome) and tracking-derived context (defender identity and distance, coverage type, exact location) that a manually scored feed does not have. See [`docs/data_dictionary/README.md`](docs/data_dictionary/README.md) for the full event catalog, how the tables join, and which columns carry tracking context.

### 📊 Season Aggregates (Shots, Drives, Picks)

Player-season, offense-only roll-ups of the shot, drive and pick events across 293 ACB 2025-2026 games, pivoted by court zone, contest level, shot type, defensive coverage and more. See [`docs/aggregates_columns.md`](docs/aggregates_columns.md) for the full column reference and [`docs/PRIMER.md`](docs/PRIMER.md#how-the-season-aggregates-are-computed) for how they're built.

## ⚠️ Limitations

TRACKING
* ~76-83% of player positions per game are directly detected on screen (`isDetected`); the remainder are extrapolated. Mean `predError` across all positions is ~1.5-1.9 ft per game (95th percentile ~4.9-6.3 ft); extrapolated positions alone average ~4.4-5.2 ft.
* Some speed or acceleration smoothing and control should be applied to the raw tracking data before use.

AGGREGATES
* The season aggregates are offense-only; there is no defensive-side data in this release.
* 293 of the 327 games of the 2025-2026 season (regular season and playoffs) are included; the missing games are mostly the playoffs plus a few regular-season fixtures. The 10 sample games are part of those 293, but the aggregates cannot be reproduced from the 10 per-game event files alone.
* Rows are per player-team-season; traded players also get a season-total row (`team_name` = "total"). See [`docs/aggregates_columns.md`](docs/aggregates_columns.md).

### Known data issues

Short version; details in [`docs/KNOWN_ISSUES.md`](docs/KNOWN_ISSUES.md).

* A few players carry two `player_id` values across the season. Use `data/player_id_aliases.csv` to merge them.
* Compute team scores from `shots` and `free_throws`, not from `chances.ptsScored`.
* `shots` includes fouled misses (not counted as attempts in box scores); picks aggregates count direct picks only.
* Some event fields are noisy (e.g. `passes.toReceiverId` holds the intercepting defender). Scores are unaffected.

## 🏗️ Repository Structure & Contributing

* **`data/`**: strictly for datasets. `data/matches/` for raw per-game tracking and event data, `data/aggregates/` for the season-level aggregate CSVs.
* **`docs/`**: the primer, the data dictionary, and the aggregate column reference.

## Contact us

* If you have feedback or research you'd like to conduct with this data, reach us on [our website](https://skillcorner.com/#contact-section) or on [Twitter](https://twitter.com/skillcorner).
* If you're interested in our product and want commercial information, contact us on [our website](https://skillcorner.com/#contact-section).
