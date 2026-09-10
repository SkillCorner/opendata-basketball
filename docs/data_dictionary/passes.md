# passes

Every pass attempt, complete or not, with the passer's and receiver's (or intended receiver's) location and court region at release, whether it led to a shot or an assist opportunity, and whether it was a turnover.

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`, `touchId`. `passerId`, `receiverId` / `toReceiverId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the pass. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `startFrame` | integer | Frame (at 25fps) since the start of the video of the release of the pass. | No |
| `endFrame` | integer | Frame (at 25fps) since the start of the video of the reception of the pass. | No |
| `startWallClock` | integer | Time in ms between the release of the pass and the start of the video. | No |
| `endWallClock` | integer | Time in ms between the reception of the pass and the start of the video. | No |
| `startGameClock` | float | Game clock in seconds at the release of the pass. | No |
| `endGameClock` | float | Game clock in seconds at the reception of the pass. | No |
| `shotClock` | float | Number of seconds left on shot clock. | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | No |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | No |
| `passerId` | integer | SkillCorner Passer Player ID. | No |
| `receiverId` | integer | SkillCorner Player ID of the receiver if the pass is not turned over. | No |
| `toReceiverId` | integer | SkillCorner Player ID of the **defender who intercepted the pass**, populated only when the pass is turned over (null otherwise). Despite the name, it is not the intended receiver — treat it as "who took the ball away", not "who the pass was meant for". | No |
| `complete` | boolean | 1 if the pass is complete, 0 otherwise. | No |
| `turnover` | boolean | 1 if the pass is turned over, 0 otherwise. | No |
| `ledToShot` | boolean | 1 if the receiver takes a shot in the touch following the pass. | No |
| `assistOpp` | boolean | 1 if the receiver takes a shot in the touch following the pass and within 3s after the reception. | No |
| `inbounds` | boolean | 1 if the pass is a throw-in from a game clock stopped, 0 otherwise. | No |
| `backcourt` | boolean | 1 if the passer is backcourt when releasing the pass, 0 otherwise. | No |
| `passerLoc` | list[float] | x, y coordinate of the passer at the release of the pass. | No |
| `receiverLoc` | list[float] | x, y coordinate of the receiver at the release of the pass. | No |
| `passerRegion` | string | Region of the passer at the release of the pass. | No |
| `receiverRegion` | string | Region of the receiver at the release of the pass. | No |
| `distance` | float | Distance in feet between passerLoc and receiverLoc | No |
| `touchId` | string | SkillCorner Touch ID | No |
