# drives

Dribble-drive events toward the basket: how the drive was created (`category`: off a pick, handoff, off-ball screen, isolation, closeout, or miscellaneous), the direction taken, whether the ball handler blew by the defender, and how the drive ended (`endType`: kick-out, pull-up, interior pass, shot near the basket, turnover, pull-out).

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`, `touchId`. `ballhandlerId`, `ballhandlerDefId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the drive | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `startGameClock` | float | Game clock in seconds at the start of the drive. | No |
| `startFrame` | integer | Frame (at 25fps) since the start of the video of the start of the drive. | No |
| `startWallClock` | integer | Time in ms between the start of the drive and the start of the video. | No |
| `endGameClock` | float | Game clock in seconds at the end of the drive. | No |
| `endFrame` | integer | Frame (at 25fps) since the start of the video of the end of the drive. | No |
| `endWallClock` | integer | Time in ms between the end of the drive and the start of the video. | No |
| `direct` | boolean | True if the drive ends with a shoot, a foul, a turnover or a direct shoot following a pass from the driver | No |
| `location` | list | Location of the start of the drive | No |
| `region` | string | Region of the drive at the start of the drive | No |
| `endLoc` | list | Location at the end of the drive | No |
| `shotClock` | float | Shot clock in seconds at the start of the drive. | No |
| `ballhandlerId` | integer | SkillCorner Ball Handler Player ID. | No |
| `ballhandlerDefId` | integer | SkillCorner Player ID of the ball handler's defender | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | No |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | No |
| `category` | string | Defines how the drives started.<br>Possible values: pick, handoff, offBallScreen, iso, closeout, miscellaneous | No |
| `blowby` | boolean | Boolean stating if the driver blew by his defender | No |
| `endType` | string | Define how the drive ended. Possible values: kickout,turnover,pullout,pullup,interiorPass,shotNearBasket | No |
| `direction` | string | Direction the driver took, left or right. | No |
| `bhrOutcomes` | list | Outcomes achieved by the Ball Handler. See outcomes definitions in touches. | No |
| `dribbleThrough` | boolean | Boolean. True if the driver dribbles through the key. | No |
| `touchId` | string | SkillCorner ID of the associated touch | No |
