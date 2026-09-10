# posts

Post-up plays: a ball handler establishing and working from the post, with the court section (left, middle, right), whether they dribbled into the post-up versus caught it near the block, and the outcome.

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`, `touchId`. `ballhandlerId`, `ballhandlerDefId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the post. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1}. | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `startGameClock` | float | Game clock in seconds at the start of the post. | No |
| `startFrame` | integer | Frame (at 25fps) since the start of the video of the start of the post. | No |
| `startWallClock` | integer | Time in ms between the start of the post and the start of the video. | No |
| `endGameClock` | float | Game clock in seconds at the end of the post. | No |
| `endFrame` | integer | Frame (at 25fps) since the start of the video of the end of the post. | No |
| `endWallClock` | integer | Time in ms between the end of the post and the start of the video. | No |
| `direct` | boolean | True if the post ends with a shoot, a foul, a turnover or a direct shoot following a pass from the ball handler | No |
| `location` | list | Location of the start of the post. | No |
| `region` | string | Region at the start of the post. | No |
| `endLoc` | list | Location at the end of the post. | No |
| `shotClock` | float | Shot clock in seconds at the start of the post. | No |
| `ballhandlerId` | integer | SkillCorner Ball Handler Player ID. | No |
| `ballhandlerDefId` | integer | SkillCorner Player ID of the ball handler's defender | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | No |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | No |
| `bhrOutcomes` | list | Outcomes achieved by the Ball Handler. See outcomes definitions in touches. | No |
| `section` | string | Section of the court where the post occured. Possible values : left, middle, right | No |
| `dribbledInto` | boolean | True if the ball handler dribbles into the postup instead of catching near the block | No |
| `touchId` | string | SkillCorner ID of the associated touch | No |
