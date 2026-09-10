# turnovers

Every live-ball and dead-ball turnover (steals, offensive fouls counted separately in `fouls`, shot-clock/backcourt/other violations), with the player who lost the ball and, for steals, the player who took it.

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`, `touchId`. `turnedOverId`, `stealerId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the turnover. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `gameClock` | float | Game clock in seconds at the turnover. | No |
| `frame` | integer | Frame (at 25fps) since the start of the video of the turnover. | No |
| `wallClock` | integer | Time in ms between the turnover and the start of the video. | No |
| `offTeamId` | integer | SkillCorner Team ID of the offensive team (the team that turn over the ball). | Yes |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | Yes |
| `turnedOverId` | integer | SkillCorner Player ID of the player who turned over the ball. | Yes |
| `stealerId` | string | SkillCorner Player ID of the player that steal the ball if it's a steal. | Yes |
| `teamId` | integer | SkillCorner Team ID of the team that turn over the ball. | Yes |
| `teamTo` | boolean | 1 if it's a team turnover (24s violation for instance). 0 otherwise. | Yes |
| `location` | list[float] | x, y coordinate of the stealer if it's a steal, otherwise x, y of the player that turnover the ball. | No |
| `region` | string | Region of the stealer if it's a steal, otherwise of the player that turnover the ball. | No |
| `touchId` | string | SkillCorner Touch ID | No |
