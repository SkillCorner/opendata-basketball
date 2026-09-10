# rebounds

Every rebound opportunity following a missed field goal or free throw, flagging whether it was grabbed by a player or went out as a team rebound, and whether it was offensive or defensive.

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`, `shotId`, `touchId`. `rebounderId` joins to player ids in `game_data`. `nextChanceId` points to the chance the rebound started (usable mainly for offensive rebounds).

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner Rebound ID. | No |
| `shotId` | string | SkillCorner Shot ID of the associated shot. | Yes |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `gameClock` | float | Game clock in seconds at the rebound. | No |
| `frame` | integer | Frame (at 25fps) since the start of the video of the rebound. | No |
| `wallClock` | integer | Time in ms between the rebound and the start of the video. | No |
| `teamId` | integer | SkillCorner Team ID of the rebounder's team. | Yes |
| `rebounderId` | integer | SkillCorner Rebounder Player ID. | Yes |
| `fgReb` | boolean | 1 if the rebound comes after a shot, 0 if it comes after a free throw. | Yes |
| `rebounded` | boolean | 1 if the rebound was taken by a player, 0 if it's a team rebound (after a shot out of bound for instance) | Yes |
| `defensive` | boolean | 1 if defensive rebound. 0 if offensive. | Yes |
| `location` | list[float] | x, y coordinate of the rebounder. | No |
| `region` | string | Region of the rebounder. | No |
| `nextChanceId` | string | SkillCorner Chance ID of the next chance following the rebound. | No |
| `touchId` | string | SkillCorner Touch ID | No |
