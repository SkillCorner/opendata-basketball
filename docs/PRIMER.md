# Primer: SkillCorner basketball data

## What this data is

SkillCorner extracts player and ball positions from broadcast video using computer vision, at 25 frames per second, with no on-court hardware and no dependency on a venue's own camera system. That raw tracking is the input; everything else in this dataset is derived from it in a pipeline with three layers:

1. **Tracking data** (`tracking_data`, one file per game): x/y/z coordinates for every player and the ball, frame by frame.
2. **Dynamic Events / markings** (`chances`, `possessions`, `shots`, `picks`, `drives`, ... one file per game): a Game Intelligence model reads the tracking data and produces a structured play-by-play — every touch, pass, dribble, shot, foul, rebound, turnover, timeout, and every named action (pick-and-roll, hand-off, off-ball screen, drive, isolation, post-up, closeout), each carrying both the box-score facts (who, what, outcome) and tracking-derived context (defender identity, distance, coverage type, location) that a manual scorer's feed does not have.
3. **Season aggregates** (`data/aggregates/*.csv`): per player-season roll-ups of the Dynamic Events, offense only, built from the shots, drives and picks event tables.

For the full field list at each layer, see the [data dictionary](data_dictionary/README.md).

## Coordinate system and units

All locations (`location`, `endLoc`, `xyz`, etc., across `tracking_data` and every event table) are in **feet**, with the origin `(0, 0)` at the **center of the court**. The offensive hoop for a given event is on the negative x side, the defensive hoop on the positive x side; when a team is attacking, its left is positive y and its right is negative y. Player and ball height (`z`) is included in `tracking_data`; players are currently always tracked at `z = 0` (kept on the ground), ball `z` is positive.

Beyond raw coordinates, most events also carry a named court **region** (`left corner three`, `right wing two`, `key`, `ra`, `backcourt`, etc.) — see the full list in the [data dictionary README](data_dictionary/README.md#markings--coordinate-system).

Speeds in `tracking_data` are in feet per second. Distances derived from tracking (`distance`, `closestDefDist`, drive/closeout distances) are in feet.

## Frame rate, clocks and periods

* **Frame rate:** 25 fps. `frameIdx` (in `tracking_data`) and `frame` / `startFrame` / `endFrame` (in the event tables) all count frames at 25fps since the start of the game video, on the same index — an event's `frame` is directly the `frameIdx` of the tracking frame it happened in.
* **`period`:** starts at 1, so the first quarter is period 1 (this generalizes across competitions that play quarters vs. halves).
* **`gameClock`:** seconds remaining in the period; 0 means the period has ended.
* **`shotClock`:** seconds remaining on the shot clock at that instant.
* **`wallClock`:** elapsed time in milliseconds since the start of the game video, on the same origin in every event table and in `tracking_data` (an event's `wallClock` equals the tracking `wallClock` at its `frame`). It runs through dead time and period breaks; use `gameClock` + `period` for in-game time.

## How the season aggregates are computed

The three aggregate files (`data/aggregates/acb_shotsaggregates_20252026.csv`, `acb_drivesaggregates_20252026.csv`, `acb_picksaggregates_20252026.csv`) are player-season roll-ups built directly from the `shots`, `drives` and `picks` Dynamic Events tables, for every ACB game processed for the 2025-2026 season — not just the 10 games whose raw event files are included here. They are **offense-only**: every row is a player's own shooting, driving or ball-handling-in-a-pick production, not what they allowed on defense.

Each table pivots its underlying events by the dimensions that matter for that action — shots by court zone, shot type and contest level; drives by how they were created and how they ended; picks by defensive coverage faced. See [`aggregates_columns.md`](aggregates_columns.md) for the full column reference, and the [data dictionary](data_dictionary/README.md) pages for `shots.md` / `drives.md` / `picks.md` for the event-level fields each metric is built from.

## Typical gotchas

* **A possession is not a chance.** An offensive rebound keeps the same `possessionId` alive but starts a new `chanceId`. If you're counting "possessions" for an efficiency stat, decide up front whether you mean `possessions` or `chances` — most points-per-possession style stats in basketball analytics actually mean `chances` (each shot attempt / turnover is its own scoring opportunity).
* **Two clocks measure different things.** `gameClock` counts down within a period and stops on every whistle; `wallClock` is elapsed video time from the start of the game and never stops. Use `wallClock` (or `frame`) to line events up with tracking frames, and `gameClock` + `period` for anything that should ignore dead time.
* **Region and location both describe position but at different resolution.** `location` is exact feet; `region` is a coarse, discrete label. They can disagree slightly at zone boundaries.
* **Not every field is present for every table.** `pbp_derived` fields (see the "PBP derived" column in the data dictionary, where present) come from official play-by-play rather than tracking — most fields do not carry that flag and are computed purely from tracking data.
* **`touchId` is the connective tissue.** Many action markings (picks, drives, handoffs, ...) reference a `touchId`; go to `touches` for duration, dribble count and the assigned defender if the marking table itself doesn't have the field you need.
* **Aggregates cover the full season; raw events cover 10 games.** The season aggregate totals are built over 293 games, so they cannot be reproduced from the 10 per-game event files. The 10 published games are part of those 293, and their shot, drive and pick events are the same events the aggregates were computed from, so a player's events in these games are a strict subset of their season row.
* **Picks aggregates count direct picks only.** The `picks` aggregate table only counts pick events where `direct = true` (the ball handler or screener shot, assisted, or was fouled directly after the pick) — in ACB 2025-2026 that's about 52% of all pick events (22,080 of 42,156). Counting raw `picks` event rows gives roughly double `handler_total_picks`; filter on `direct` first.
* **Aggregate rows are per player-team-season, not per player-season.** A player traded mid-season gets one row per team plus an extra season-total row (`team_id` empty, `team_name` = `"total"`). Sum the wrong subset of rows and you'll double-count traded players. See [`aggregates_columns.md`](aggregates_columns.md#grain-and-identity-columns-all-three-tables).
* **`attempts` (shots aggregate) is a box-score number, not a raw event count.** It follows FIBA convention and excludes field goal attempts missed while the shooter was fouled (those are free throw trips, not field goal attempts) — the underlying `shots` event table includes them, so raw event counts run higher than `attempts`. `total_points` includes free throws made on and-one plays, so it isn't simply points from made field goals.
* **`games_played` counts on-court presence, not tracked activity.** It's the number of games the player was on court for at least one chance (from `chance_players`), not the number of games with a tracked shot, drive or pick — a row can have `games_played > 0` and zero attempts. It also reflects SkillCorner's delivered data, not official appearances: 293 of 327 games of the 2025-2026 season (regular season and playoffs) are included, with the missing games mostly playoffs plus a few regular-season fixtures, so teams range from 31 to 34 games in the 293-game set.
