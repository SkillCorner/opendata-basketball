# chances

A chance is one continuous stretch of offense by a team that ends in a shot attempt, a turnover, a shooting foul, an end-of-period, or a jump ball. A new chance starts after an offensive rebound even though the ball did not change teams, so a single possession can contain several chances. This is the finest-grained scoring unit in the data: every shot, foul, turnover and rebound belongs to exactly one chance.

Join keys: `id` (primary key), `gameId`, `possessionId` (parent possession). `offPlayerIds` / `defPlayerIds` list the on-court roster for the chance and join to `game_data` player ids.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the chance. | No |
| `possessionId` | integer | SkillCorner id of the associated possession. | No |
| `gameId` | string | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `startFrame` | integer | Frame (at 25fps) since the start of the video of the start of the chance. | No |
| `endFrame` | integer | Frame (at 25fps) since the start of the video of the end of the chance. | No |
| `startWallClock` | integer | Time in ms between the start of the chance and the start of the video. | No |
| `endWallClock` | integer | Time in ms between the end of the chance and the start of the video. | No |
| `startGameClock` | float | Game clock in seconds at the start of the chance. | No |
| `endGameClock` | float | Game clock in seconds at the end of the chance. | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | Yes |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | Yes |
| `startType` | string | Event that starts the chance. One of<br>        - DEFOB: Defensive Out of Bounds<br>        - FGDRB: Field Goal Defensive RB<br>        - FGORB: Field Goal Offensive RB<br>        - FTDRB: Free Throw Defensive RB<br>        - FTORB: Free Throw Offensive RB<br>        - JMP: Jump Ball<br>        - TO: Live Ball Turnover<br>        - FTM: Free Throw Made<br>        - FGM: Field Goal Made | Yes |
| `outcome` | string | Event that ends the chance. One of<br>        - FGM: Any made field goal<br>        - FGM3: Made 3 pointer<br>        - FGX: Any missed field goal<br>        - FGX3: Missed 3 pointer<br>        - TO: Turnover<br>        - VIO: Violation<br>        - JMP: Jump Ball<br>        - Out of Bounds<br>        - FOU: Foul<br>        - EPD: End of period | Yes |
| `offPlayerIds` | list[integer] | List of SkillCorner Player ID, for all players from the offensive team, on court during the chance. | Yes |
| `defPlayerIds` | list[integer] | List of SkillCorner Player ID, for all players from the defensive team, on court during the chance. | Yes |
| `homeStartScore` | integer | Home team score at the start of the chance. | Yes |
| `awayStartScore` | integer | Away team score at the start of the chance. | Yes |
| `ptsScored` | integer | Points scored in the chance. | Yes |
| `startShotClock` | float | Shot clock in seconds at the start of the chance. | No |
| `endShotClock` | float | Shot clock in seconds at the end of the chance. | No |
| `ballInPaint` | boolean | Boolean that determines if a player possess the ball in paint - either through dribbling, rebound or touch. | No |
| `endOfPossession` | boolean | True if the chance is the last one of the possession. False otherwise. | Yes |
| `endLoc` | list[float] | x, y location of the end of the chance. | No |
| `frontcourtFrame` | integer | First frame during the chance where the ball is possessed in the front court. | No |
| `transition` | boolean | True if the chance is a transition. False otherwise. | No |
| `lastChanceId` | string | SkillCorner chance ID of the previous chance. | No |
| `qualityIndex` | integer | SkillCorner quality index of the chance. Number between 0 (lowest quality) and 5 (highest quality). | No |
| `usable` | boolean | Boolean that is equal to true if qualityIndex is greater or equal to 3. | No |
