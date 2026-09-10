# touches

Every continuous ball possession by a single player (from gaining control to losing it), with duration, number of dribbles, start/end location, the defender assigned at the start of the touch, and a list of `outcomes` (pass, shot made/missed, assist, foul, turnover, timeout, etc.). Touches are the reference event for the `outcomes` / `bhrOutcomes` / `scrOutcomes` enum used across picks, drives, handoffs, isolations, posts, off-ball screens and closeouts.

Join keys: `id` (primary key, referenced as `touchId` elsewhere), `gameId`, `chanceId`, `possessionId`. `playerId`, `defenderId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the touch. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `startFrame` | integer | Frame (at 25fps) since the start of the video of the start of the touch. | No |
| `endFrame` | integer | Frame (at 25fps) since the start of the video of the end of the touch. | No |
| `startWallClock` | integer | Time in ms between the start of the touch and the start of the video. | No |
| `endWallClock` | integer | Time in ms between the end of the touch and the start of the video. | No |
| `startGameClock` | float | Game clock in seconds at the start of the touch. | No |
| `endGameClock` | float | Game clock in seconds at the end of the touch. | No |
| `shotClock` | float | Number of seconds left on shot clock. | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | No |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | No |
| `playerId` | integer | SkillCorner Player ID. | No |
| `defenderId` | integer | SkillCorner Defender Player ID. <br>Defender is the player assigned to the player in the rotation at the start if a rotation exist (ball is frontcourt).<br>Otherwise, it's the closest player in average for the duration of the touch. | No |
| `closestDefLoc` | list[float] | x, y coordinate of the defender at the start of the touch. | No |
| `location` | list[float] | x, y coordinate of the player at the start of the touch. | No |
| `endLoc` | list[float] | x, y coordinate of the player at the end of the touch. | No |
| `numDribbles` | integer | Number of dribbles occuring during the touch | No |
| `ledToShot` | boolean | 1 if the player has taken a shot within the touch, 0 otherwise. | No |
| `touchTime` | float | Duration of the touch in seconds. | No |
| `outcomes` | list[string] | Outcome by the ballhandler. List of items from:<br>- PASS: Pass<br>- PASS_SCR: Pass to screener (on picks & handoffs)<br>- FGM: Field goal made<br>- FGM3: Made 3 pointer<br>- FGX: Missed field goal<br>- FGX3: Missed 3 pointer<br>- BLK: Blocked shot<br>- FOUL: Foul<br>- AST: Assist (pass made to a teammate who took the shot within one dribble)<br>- AST3: Assist for a three pointer<br>- AST2: Assist for a two pointer<br>- AST0: Assist opportunity missed by the teammate<br>- ASTF: Assist opportunity ending with teammate fouled during shot<br>- TO: Turnover<br>- FOUL: Any foul<br>- FOU_S: Shooting Foul<br>- FOU_T: Technical foul<br>- FOU_F: Flagrant Foul<br>- FOU_B: Foul in the bonus<br>- FOU_N: Personal foul that is neither shooting nor in the bonus<br>- FOU_O: Offensive Foul<br>- TMO: Timeout | No |
| `regionsIn` | list[string] | List of the region of the player during the touch. | No |
| `endClosestDefLoc` | list[float] | x, y coordinate of the defender at the end of the touch. | No |
| `direct` | boolean | True if the ballhandler shoots, is fouled and shoots free throws, turns the ball over, or if they pass to another player who shoots within one dribble of receiving the ball. | No |
