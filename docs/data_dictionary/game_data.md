# game_data

Per-game metadata: identifiers for the game, competition, edition and season, tip-off time, last processing timestamps for tracking, Dynamic Events and physical data, and the home/away team rosters. Delivered as `{gameId}_game_data.json`, a single JSON object of roughly 2 KB. One `game_data` record exists per game and is the anchor every other table's `gameId` points back to.

**Grain:** one row per game. **Join key:** `gameId` joins to every other table's `gameId` field. `homeTeam.players[i].playerId` / `awayTeam.players[i].playerId` join to the player id fields used across the event tables (`shooterId`, `ballhandlerId`, `playerId`, etc.).

| Field | Type | Definition |
|---|---|---|
| `gameId` | integer | SkillCorner Game ID. |
| `date` | datetime | Official scheduled tip-off in UTC (format: `YYYY-MM-DDTHH:MM:SSZ`). Same value as `date_time` in `data/matches.json`. Tracking may start slightly before or after this instant. |
| `competitionEditionId` | integer | SkillCorner CompetitionEdition ID. |
| `competitionId` | integer | SkillCorner Competition ID. |
| `competitionName` | string | SkillCorner Competition Name. |
| `seasonId` | integer | SkillCorner Season ID. |
| `seasonName` | string | SkillCorner Season Name. |
| `trackingLastProcessingDate` | datetime | Last processing datetime of the tracking data, in UTC (format: `YYYY-MM-DDTHH:MM:SSZ`). |
| `dynamicEventsLastProcessingDate` | datetime | Last processing datetime of the Dynamic Events, in UTC (format: `YYYY-MM-DDTHH:MM:SSZ`). |
| `physicalLastProcessingDate` | datetime | Last processing datetime of the physical (speed/load) data, in UTC (format: `YYYY-MM-DDTHH:MM:SSZ`). |
| `homeTeam.teamId` | integer | SkillCorner home team ID. |
| `homeTeam.teamName` | string | Home team name. |
| `homeTeam.players` | list[object] | List of the home team's players, see "Player object" below. |
| `awayTeam.teamId` | integer | SkillCorner away team ID. |
| `awayTeam.teamName` | string | Away team name. |
| `awayTeam.players` | list[object] | List of the away team's players, see "Player object" below. |

## Player object (`homeTeam.players[i]` / `awayTeam.players[i]` entries)

| Field | Type | Definition |
|---|---|---|
| `playerId` | integer | SkillCorner Player ID. |
| `firstName` | string | Player first name. |
| `lastName` | string | Player last name. |
| `jersey` | string | Jersey number of the player. |

Player position is not published in `game_data.json`.
