# free_throws

Every free throw attempt, linked to the foul (and, if applicable, the shot) that awarded it, with the shooter and the make/miss outcome.

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`, `foulId`, `shotId`. `shooterId` joins to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the free throw. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `gameClock` | float | Game clock in seconds at the free throw. | No |
| `frame` | integer | Frame (at 25fps) since the start of the video of the free throw. | No |
| `wallClock` | integer | Time in ms between the free throw and the start of the video. | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | Yes |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | Yes |
| `shooterId` | integer | SkillCorner Shooter Player ID. | Yes |
| `outcome` | boolean | 1 if the free throw is scored, 0 if it's missed. | Yes |
| `foulId` | string | SkillCorner Foul ID associated to this free_throw. | No |
| `shotId` | string | SkillCorner Shot ID if this free throw is associated to a foul on a shot. | No |
