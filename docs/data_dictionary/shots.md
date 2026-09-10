# shots

Every field goal attempt, with the shooter's location and shot zone at release, the type of shot (catch-and-shoot, off-dribble, post, etc.), the contest level and closest defender, and the outcome (made/missed, assisted, blocked, fouled).

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`, `touchId` (the touch the shot was taken from). `shooterId`, `passerId`, `blockerId`, `closestDefId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the shot. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `startFrame` | integer | Frame (at 25fps) since the start of video of the release of the shot. | No |
| `startWallClock` | integer | Time in ms between the release of the shot and the start of the video. | No |
| `startGameClock` | float | Game clock in seconds at the release of the shot. | No |
| `endFrame` | integer | Frame (at 25fps) since the start of the video of the end of the shot. | No |
| `endWallClock` | integer | Time in ms between the end of the shot and the start of the video. | No |
| `endGameClock` | float | Game clock in seconds at the end of the shot. | No |
| `location` | list[float] | x, y coordinate of the shooter at the release of the shot. | No |
| `region` | string | Region of the shooter at the release of the shot. | No |
| `shotClock` | float | Number of seconds left on shot clock | No |
| `shooterId` | integer | SkillCorner Shooter Player ID. | Yes |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | Yes |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | Yes |
| `three` | boolean | true if the shot is a 3 points shot, false if it's a 2 point shot. | Yes |
| `outcome` | boolean | true if the shot is scored, false if it's missed. | Yes |
| `fouled` | boolean | true if the shot is fouled, false otherwise. | Yes |
| `foulId` | string | Skillcorner Foul ID if the shot has been fouled. | No |
| `assisted` | boolean | true if the shot is assisted, false otherwise. | Yes |
| `assistOpp` | boolean | true if the shot is assisted or is taken less than 3s after the reception of a pass, false otherwise. | No |
| `passerId` | string | SkillCorner Player ID of the player that passed to the shooter. Null if no passer before the shot. | Yes |
| `blocked` | boolean | true if the shot is blocked, false otherwise. | Yes |
| `blockerId` | integer | SkillCorner Blocker Player ID. | Yes |
| `distance` | float | Distance between the shooter and the hoop at time of release, in feet. | No |
| `dribblesBefore` | integer | Number of dribbles before the shot | No |
| `shotType` | string | Simple breakdown of the shot. <br>Possible values are: jumper, floater, layup, post, heave. | No |
| `complexShotType` | string | Advanced breakdown of the shot. <br>Possible values : floater,layup,heave,catchAndShoot,offMove,dribblePullUp,shakeAndRaise,stepback,leaner,postFadeaway,hook,lob,tip,dunk | No |
| `catchAndShoot` | boolean | true if releaseTime <= 1.5s OR complexShotType = 'catchAndShoot' | No |
| `createdFromPaint` | boolean | true if the shot comes directly from a touch in the paint or a dribble into paint and shoot or a pass from paint to shoot | No |
| `contested` | boolean | true if the shot has a contestLevel equal to average, plus or blocked | No |
| `contestLevel` | string | Defines the level of contest of a shot.<br>Possible values: open,light,average,plus,blocked | No |
| `releaseTime` | float | Number of seconds from the start of the touch to the shooter’s release | No |
| `shotQuality` | float | SkillCorner shot quality score for the attempt, on a 0-100 scale. Null on a small number of attempts the model could not score. | No |
| `closestDefDist` | float | Distance between the shooter and its closest defender at time of release, in feet. | No |
| `closestDefId` | string | SkillCorner Closest Defender Player ID. | No |
| `touchId` | string | SkillCorner Touch ID | No |
