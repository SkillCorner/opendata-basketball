# Data dictionary

Field-level reference for every table in this dataset. One file per table:

**Match context**

* [`game_data`](game_data.md) — game, competition, season identifiers and team rosters.
* [`tracking_data`](tracking_data.md) — broadcast optical tracking, 25fps, per-game.

**Core play-by-play structure**

* [`possessions`](possessions.md) — one continuous span of team control of the ball.
* [`chances`](chances.md) — one continuous scoring opportunity within a possession (a possession spans several chances when the offense keeps the ball alive off an offensive rebound).
* [`chance_players`](chance_players.md) — on-court participation, one row per player per chance.
* [`matchups`](matchups.md) — who is guarding whom, as time intervals within a chance.

**Outcome events** (every made/missed shot, turnover, foul etc. belongs to exactly one chance)

* [`shots`](shots.md), [`free_throws`](free_throws.md), [`rebounds`](rebounds.md), [`turnovers`](turnovers.md), [`fouls`](fouls.md), [`timeouts`](timeouts.md)

**Ball-movement events** (the mechanics of how a chance developed)

* [`passes`](passes.md), [`touches`](touches.md), [`dribbles`](dribbles.md)

**Action markings** (named actions a team runs, each carrying tracking-derived defensive context)

* [`picks`](picks.md), [`handoffs`](handoffs.md), [`off_ball_screens`](off_ball_screens.md), [`drives`](drives.md), [`isolations`](isolations.md), [`posts`](posts.md), [`closeouts`](closeouts.md)

## How the tables join

Everything hangs off four keys:

* **`gameId`** — every table carries it; joins any table to [`game_data`](game_data.md) for date, competition, season and rosters.
* **`possessionId`** — the parent [`possessions`](possessions.md) row for a chance or event.
* **`chanceId`** — the parent [`chances`](chances.md) row for an event. A chance is the unit almost everything else hangs off: `offPlayerIds` / `defPlayerIds` on `chances` give the on-court lineup, `startType` / `outcome` give how it began and ended, `qualityIndex` / `usable` flag tracking-data confidence.
* **Player ids** — every table uses integer SkillCorner player ids (named contextually: `shooterId`, `ballhandlerId`, `screenerId`, `passerId`, `rebounderId`, `foulerId`, `defPlayerId`, ...). All of them join to `homeTeam.players[i].playerId` / `awayTeam.players[i].playerId` in [`game_data`](game_data.md).

A secondary key, **`touchId`**, links an action marking (a pick, a drive, a shot, ...) back to the [`touches`](touches.md) row it happened within — useful for pulling touch-level context (duration, dribble count, defender at catch) for any event.

Region and shot-zone strings are shared across tables and use the same court-region vocabulary — see the region list below.

## Event families

* **Core events** — `possessions`, `chances`, `shots`, `free_throws`, `rebounds`, `turnovers`, `fouls`, `timeouts`, `passes`, `touches`, `dribbles`. These record what happened and to whom, independent of tracking data.
* **Action markings** — `picks`, `handoffs`, `off_ball_screens`, `drives`, `isolations`, `posts`, `closeouts`. These are named plays SkillCorner's Game Intelligence models detect from the tracking data: a pick-and-roll, a dribble hand-off, an off-ball screen for a cutter, a drive, an isolation, a post-up, a defensive closeout. They all carry two players (the primary actor and, where relevant, a screener/setter/cutter) plus each player's defender and the defensive coverage called.
* **Player tracking-derived context** — `chance_players` (on-court presence, matchups, shot/rim/rebound locations, minutes played) and `matchups` (defensive assignment over time). These are what makes it possible to say who was guarding whom for any given event.
* **Game context** — `game_data` (game/competition/season identity, rosters) and `tracking_data` (raw player and ball positions at 25fps).

## Columns that carry tracking context

These are the fields that make this dataset different from a plain play-by-play feed — they come from the optical tracking, not from a scorer's keyboard:

* **`picks` / `handoffs` / `off_ball_screens`**: `ballhandlerDefId` / `screenerDefId` / `cutterDefId` / `setterDefId` (who was guarding whom, tracked through any switch), `bhrDefType` / `scrDefType` / `receiverDefType` / `setterDefType` / `cutterDefType` / `screenerDefType` (defensive coverage: e.g. `ice`, `switch`, `blitz`, `drop`-style `soft`/`show`, `trail`, `whip`, `ride`, `top lock`, `jam`), `location` / `region` / `locationType` (where on the court, in feet and in named regions).
* **`shots`**: `closestDefDist` / `closestDefId` (distance to and identity of the nearest defender at release, in feet), `contestLevel` / `contested` (`open`, `light`, `average`, `plus`, `blocked`), `distance` (shooter-to-hoop distance at release), `releaseTime` (seconds from touch start to release).
* **`closeouts`**: `startDistance` / `touchDistance` / `endDistance` (ball handler-to-defender distance at three checkpoints of the closeout) and each checkpoint's `startLoc` / `touchLoc` / `endLoc`.
* **`touches`**: `closestDefLoc` / `endClosestDefLoc` (defender position at the start and end of the touch), `defenderId` (assigned matchup defender, or nearest defender if no rotation exists).
* **`chance_players`**: `startMatchupId` / `endMatchupId` (tracked defensive assignment at the start/end of the chance), `shotLoc` / `rimLoc` / `reboundLoc` (player position at three tracked moments).
* **`drives`**: `blowby` (whether the driver beat their defender), `direction`, `dribbleThrough`.

## Markings / coordinate system

Location is delivered as `[x, y]` in feet, `(0, 0)` at the center of the court. The offensive hoop is at negative x, the defensive hoop at positive x. When attacking, the left side of the court is positive y, the right side is negative y. This convention is shared by every `location` / `endLoc` / `passerLoc` / `receiverLoc` field across the event tables, and is the same coordinate system used by `tracking_data`.

Region strings (used in `region`, `passerRegion`, `receiverRegion`, etc.) take one of: `left corner three`, `left corner two`, `left wing three`, `left wing two`, `backcourt`, `far`, `middle three`, `middle two`, `key`, `ra` (restricted area), `right wing three`, `right wing two`, `right corner three`, `right corner two`.

Markings data (everything except `tracking_data` and `game_data`) is delivered as a single JSON file per game (`{gameId}_dynamic_events.json`), keyed by marking type — exactly these 20 keys: `possessions`, `chances`, `chance_players`, `matchups`, `shots`, `free_throws`, `rebounds`, `turnovers`, `fouls`, `timeouts`, `passes`, `touches`, `dribbles`, `picks`, `handoffs`, `off_ball_screens`, `drives`, `isolations`, `posts`, `closeouts` (the `matchups` key holds the table documented in [`matchups.md`](matchups.md)); each key's value is the list of that marking type's events for the game, with the fields documented on its own page above.

## Known type quirks

* **`closeouts.touchWallClock`** is delivered as a **string** (e.g. `"97080"`), while the sibling `startWallClock` / `endWallClock` on the same table are integers. Cast it before doing arithmetic on it.
