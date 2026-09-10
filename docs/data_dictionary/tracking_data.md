# tracking_data

Broadcast optical tracking data for one game, delivered as `{gameId}_tracking_data.jsonl.gz` (gzip-compressed JSON Lines, one JSON object per "frame" of video). Each line gives the position of every tracked player and the ball at 25 frames per second, plus the game clock, shot clock and period at that instant. This is the raw spatial signal all Dynamic Events (chances, shots, picks, drives, etc.) are derived from.

**Grain:** one row per frame per game. **Join key:** `frameIdx` / `wallClock` / `gameClock` + `period` line up with the `frame` / `wallClock` / `gameClock` fields used across the event tables (picks, shots, drives, ...) to locate the tracking context of an event.

**Coordinate system:** all `xyz` coordinates are in feet, origin `(0, 0)` at the center of the court. See [Markings](README.md#markings--coordinate-system) for the shared court coordinate convention (also used by every `location` / `endLoc` field in the event tables).

**Dead time:** roughly half of all frames in a game (dead ball, warmups, breaks) carry empty `homePlayers`/`awayPlayers` arrays and an empty `ball` object, `{}`. Clock fields (`gameClock`, `shotClock`, `gameClockStopped`, `period`) stay populated on these rows, so the frame timeline itself is continuous even though player/ball data is not — don't assume every row has 10 players and a ball.

## Top-level fields

| Field | Type | Definition |
|---|---|---|
| `frameIdx` | integer | Frame count (at 25fps) since the start of the video. |
| `wallClock` | integer | Time in ms since the start of the video. |
| `gameClock` | float | Game clock in seconds. 0 means the period is finished. |
| `gameClockStopped` | boolean | `true` if the game clock is stopped, `false` if the game clock is running. |
| `period` | integer | Number of the period (starts at 1, so the first quarter/period is 1). |
| `homePlayers` | list[object] | List of player positions at this frame for the home team. Empty on dead-time frames. See "Player object" below. |
| `awayPlayers` | list[object] | List of player positions at this frame for the away team. Empty on dead-time frames. See "Player object" below. |
| `ball` | object | Ball position at this frame. `{}` (empty object) on dead-time frames. See "Ball object" below. |
| `shotClock` | float | Shot clock in seconds. Can be `null` (e.g. before the first frontcourt possession of a period). |

## Player object (`homePlayers` / `awayPlayers` entries)

| Field | Type | Definition |
|---|---|---|
| `xyz` | list[float] | Coordinate of the player in feet: x along the length of the court (left to right from the camera's point of view, 0 at court center); y along the width of the court (bottom to top from the camera's point of view, 0 at court center); z is height, currently always 0 (players are kept on the ground). |
| `speed` | float | Player speed in feet per second. |
| `jersey` | string | Jersey number of the player. |
| `playerId` | integer | SkillCorner Player ID. |
| `isDetected` | integer (0 or 1) | `1` if the player is on screen and detected by computer vision, `0` if the position is extrapolated. (Note the ball object below delivers the same flag as a float.) |
| `predError` | float | Expected error for the player's coordinate, in feet. In 90% of cases the tracking is within `predError` feet of ground truth. Across the 10 published games the mean is ~1.5-1.9 ft over all positions (95th percentile ~4.9-6.3 ft); detected positions average ~0.9 ft, extrapolated positions ~4.4-5.2 ft. |

## Ball object

| Field | Type | Definition |
|---|---|---|
| `xyz` | list[float] | Coordinate of the ball in feet, same convention as the player `xyz` above; z (height) is a real height and can go slightly negative near the floor (calibration noise), not always positive. |
| `speed` | float | Ball speed in feet per second. |
| `isDetected` | float (0.0 or 1.0) | `1.0` if the ball is on screen and detected by computer vision, `0.0` if the position is extrapolated. Same meaning as the player-object `isDetected`, but delivered as a float here instead of an integer — normalize both to boolean on ingest if you need a consistent type. |
| `predError` | float | Expected error for the ball's coordinate, in feet. Ball calibration is not as accurate as player calibration. |

Delivered as gzip-compressed JSON Lines: each line of the decompressed file is one frame. Decompress with `gzip -d`, or read directly with `pandas.read_json(path, lines=True, compression="gzip")`.
