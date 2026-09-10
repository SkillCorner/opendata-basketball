# fouls

Every personal, technical, offensive and flagrant foul, with the fouler and the fouled player, whether it happened on a shot, whether the fouled team was in the bonus, and the foul type.

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`, `touchId`, `shotId`. `foulerId`, `fouledId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the foul. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `gameClock` | float | Game clock in seconds at the foul. | No |
| `frame` | integer | Frame (at 25fps) since the start of the video of the foul. | No |
| `wallClock` | integer | Time in ms between the foul and the start of the video. | No |
| `foulerId` | integer | SkillCorner Player ID of the player that has committed the foul. | Yes |
| `fouledId` | integer | SkillCorner Player ID of the player that has been fouled. | Yes |
| `foulerTeamId` | integer | SkillCorner Team ID of the team of the player that has committed the foul. | Yes |
| `fouledTeamId` | integer | SkillCorner Team ID of the team of player that has been fouled. | Yes |
| `shooting` | boolean | 1 if the foul happens during a shot, 0 otherwise. | Yes |
| `location` | list[float] | x, y coordinate of the fouler. | No |
| `region` | string | Region of the fouler. | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | Yes |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | Yes |
| `foulType` | string | Define the foul type. | Yes |
| `isBonus` | boolean | Define if the opposing team is a bonus situation. | Yes |
| `isTeam` | boolean | Define if the foul is a team foul. | Yes |
| `isTechnical` | boolean | Define if the foul is a technical foul. | Yes |
| `touchId` | string | SkillCorner Touch ID. | No |
| `shotId` | string | SkillCorner Shot ID if foul associated foul happened during a shot. | No |
