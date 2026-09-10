# chance_players

One row per player per chance, recording whether the player was on offense or defense, their assigned matchup at the start and end of the chance, their location at shot release / at the rim / at the rebound (when applicable), and their cumulative minutes played entering the chance. This is the table to use for on-court participation and for joining tracking-derived matchup data to a chance.

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`. `playerId`, `startMatchupId`, `endMatchupId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the touch. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | Yes |
| `possessionId` | string | SkillCorner id of the associated possession. | Yes |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `playerId` | integer | SkillCorner Player ID. | Yes |
| `offense` | boolean | 1 if player is in offense, 0 otherwise. | Yes |
| `startMatchupId` | integer | SkillCorner Player ID of the matchup player at the start of the chance (from the rotation). | No |
| `endMatchupId` | integer | SkillCorner Player ID of the matchup player at the end of the chance (from the rotation). | No |
| `shotLoc` | list[float] | x, y coordinate of the player at release of the shot. | No |
| `rimLoc` | list[float] | x, y coordinate of the player when the ball reaches the rim.  Null if no shot occurs. | No |
| `reboundLoc` | list[float] | x, y coordinate of the player at rebound. | No |
| `minutesPlayedBefore` | float | Minutes played by the player at the start of the chance | No |
