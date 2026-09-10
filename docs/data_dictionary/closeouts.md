# closeouts

Defensive closeout events: a defender running out to contest a ball handler who just caught the ball, with the defender's location and the ball handler-defender distance at three checkpoints (start of the touch, start of the closeout, end of the closeout), and what the ball handler did after the catch.

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`, `touchId`. `ballhandlerId`, `ballhandlerDefId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the closeout. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1}. | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `touchGameClock` | float | Game clock in seconds at the start of the touch. | No |
| `touchFrame` | integer | Frame (at 25fps) since the start of the video of the start of the touch. | No |
| `touchWallClock` | integer | Time in ms between the start of the touch and the start of the video. | No |
| `startGameClock` | float | Game clock in seconds at the start of the closeout. | No |
| `startFrame` | integer | Frame (at 25fps) since the start of the video of the start of the closeout. | No |
| `startWallClock` | integer | Time in ms between the start of the closeout and the start of the video. | No |
| `endGameClock` | float | Game clock in seconds at the end of the closeout. | No |
| `endFrame` | integer | Frame (at 25fps) since the start of the video of the end of the closeout. | No |
| `endWallClock` | integer | Time in ms between the end of the closeout and the start of the video. | No |
| `direct` | boolean | True if the closeout ends with a shoot, a foul, a turnover or a direct shoot following a pass from the ball handler | No |
| `location` | list | Location of the ball handler at the start of the touch. | No |
| `region` | string | Region at the start of the touch. | No |
| `startLoc` | list | Defender's location at the start of the closeout. | No |
| `endLoc` | list | Defender's location at the end of the closeout. | No |
| `touchLoc` | list | Defender's location at the start of the touch. | No |
| `startDistance` | float | Distance between the ball handler and his defender at the start of the closeout. | No |
| `touchDistance` | float | Distance between the ball handler and his defender at the start of the touch. | No |
| `endDistance` | float | Distance between the ball handler and his defender at the end of the closeout. | No |
| `ballhandlerId` | integer | SkillCorner Ball Handler Player ID. | No |
| `ballhandlerDefId` | integer | SkillCorner Player ID of the ball handler's defender | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | No |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | No |
| `bhrOutcomes` | list | Outcomes achieved by the Ball Handler. See outcomes definitions in touches. | No |
| `bhrAction` | string | Ball handler action after the catch. Possible values: shot, drive, pass, other. | No |
| `touchId` | string | SkillCorner ID of the associated touch. | No |
