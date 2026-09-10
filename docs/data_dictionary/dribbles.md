# dribbles

Individual dribble events, one row per dribble, nested inside a `touches` row. Gives the ball handler's location and court region at each dribble.

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`, `touchId`. `ballhandlerId` joins to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the dribble | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `gameClock` | float | Game clock in seconds at the dribble. | No |
| `frame` | integer | Frame (at 25fps) of the dribble | No |
| `wallClock` | integer | Time in ms between the dribble and the start of the video. | No |
| `ballhandlerId` | integer | SkillCorner Ball Handler Player ID. | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | No |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | No |
| `location` | list[float] | x, y coordinate of the ball handler. | No |
| `region` | string | Region of the ball handler. | No |
| `touchId` | string | SkillCorner Touch ID | No |
