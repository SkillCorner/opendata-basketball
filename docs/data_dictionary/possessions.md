# possessions

A possession is the full continuous span of team control of the ball, from the moment a team gains it to the moment the other team gains it (a made or dead-ball turnover, defensive rebound, end of period). A possession can contain multiple `chances` when the offense grabs an offensive rebound and keeps the ball alive.

Join keys: `id` (primary key), `gameId`. `offPlayerIds` / `defPlayerIds` can include more than 5 players per team if there were in-possession substitutions.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the possession. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `startFrame` | integer | Frame (at 25fps) since the start of the video of the start of the possession. | No |
| `endFrame` | integer | Frame (at 25fps) since the start of the video of the end of the possession. | No |
| `startWallClock` | integer | Time in ms between the start of the possession and the start of the video. | No |
| `endWallClock` | integer | Time in ms between the end of the possession and the start of the video. | No |
| `startGameClock` | float | Game clock in seconds at the start of the possession. | No |
| `endGameClock` | float | Game clock in seconds at the end of the possession. | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | Yes |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | Yes |
| `startType` | string | Event that starts the chance. One of<br>        - DEFOB: Defensive Out of Bounds<br>        - FGDRB: Field Goal Defensive RB<br>        - FGORB: Field Goal Offensive RB<br>        - FTDRB: Free Throw Defensive RB<br>        - FTORB: Free Throw Offensive RB<br>        - JMP: Jump Ball<br>        - TO: Live Ball Turnover<br>        - FTM: Free Throw Made<br>        - FGM: Field Goal Made | Yes |
| `outcome` | list[string] | Event that ends the chance. One of<br>        - FGM: Any made field goal<br>        - FGM3: Made 3 pointer<br>        - FGX: Any missed field goal<br>        - FGX3: Missed 3 pointer<br>        - TO: Turnover<br>        - VIO: Violation<br>        - JMP: Jump Ball<br>        - Out of Bounds<br>        - FOU: Foul<br>        - EPD: End of period | Yes |
| `offPlayerIds` | list[integer] | List of SkillCorner Player ID, for all players from the offensive team, on court at any time during the possession.<br>Can be more than 5 players if there are substitutions within the possession. | Yes |
| `defPlayerIds` | list[integer] | List of SkillCorner Player ID, for all players from the defensive team, on court at any time during the possession.<br>Can be more than 5 players if there are substitutions within the possession. | Yes |
| `homeStartScore` | integer | Home team score at the start of the possession. | Yes |
| `awayStartScore` | integer | Away team score at the start of the possession. | Yes |
| `ptsScored` | integer | Points scored in the possession. | Yes |
| `ballInPaint` | boolean | Boolean that determines if a player possess the ball in paint - either through dribbling, rebound or touch. | No |
| `endLoc` | list[float] | x, y location of the end of the possession. | No |
| `leftHoop` | boolean | True if the offensive team is shooting at the left broadcast hoop | No |
