# timeouts

Every timeout called, with the team and the game clock at the time.

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`. `teamId` joins to the team ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the timeout. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `gameClock` | float | Game clock in seconds at the timeout. | No |
| `frame` | integer | Frame (at 25fps) since the start of the video of the timeout. | No |
| `wallClock` | integer | Time in ms between the timeout and the start of the video. | No |
| `teamId` | string | SkillCorner Team ID of the team that calls the timeout. | Yes |
