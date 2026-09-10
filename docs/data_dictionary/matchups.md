# matchups

Defensive matchup assignments over time: which defender is assigned to guard which offensive player, as a series of time intervals (`startFrame`/`endFrame`) within a chance. Multiple rows per chance when matchups switch mid-chance (e.g. after a screen).

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`. `defPlayerId`, `offPlayerId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the rotation. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `startGameClock` | float | Game clock in seconds at the start of the rotation. | No |
| `startFrame` | integer | Frame (at 25fps) since the start of the video of the start of the rotation. | No |
| `startWallClock` | integer | Time in ms between the start of the rotation and the start of the video. | No |
| `endGameClock` | float | Game clock in seconds at the end of the rotation. | No |
| `endFrame` | integer | Frame (at 25fps) since the start of the video of the end of the rotation. | No |
| `endWallClock` | integer | Time in ms between the end of the rotation and the start of the video. | No |
| `shotClock` | float | Number of seconds left on shot clock. | No |
| `defPlayerId` | integer | SkillCorner Defensive Player ID. | No |
| `offPlayerId` | integer | SkillCorner Offensive Player ID. | No |
