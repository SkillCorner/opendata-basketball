# isolations

One-on-one isolation plays: a ball handler attacking their primary defender without a screen, with start/end location and the outcome achieved by the ball handler.

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`, `touchId`. `ballhandlerId`, `ballhandlerDefId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the isolation | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `startGameClock` | float | Game clock in seconds at the start of the isolation. | No |
| `startFrame` | integer | Frame (at 25fps) since the start of the video of the start of the isolation. | No |
| `startWallClock` | integer | Time in ms between the start of the isolation and the start of the video. | No |
| `endGameClock` | float | Game clock in seconds at the end of the isolation. | No |
| `endFrame` | integer | Frame (at 25fps) since the start of the video of the end of the isolation. | No |
| `endWallClock` | integer | Time in ms between the end of the isolation and the start of the video. | No |
| `direct` | boolean | True if the isolation ends with a shoot, a foul, a turnover or a direct shoot following a pass from the ball handler | No |
| `location` | list | Location of the start of the isolation. | No |
| `region` | string | Region at the start of the isolation. | No |
| `endLoc` | list | Location at the end of the isolation. | No |
| `shotClock` | float | Shot clock in seconds at the start of the isolation. | No |
| `ballhandlerId` | integer | SkillCorner Ball Handler Player ID. | No |
| `ballhandlerDefId` | integer | SkillCorner Player ID of the ball handler's defender | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | No |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | No |
| `bhrOutcomes` | list | Outcomes achieved by the Ball Handler. See outcomes definitions in touches. | No |
| `touchId` | string | SkillCorner ID of the associated touch | No |
