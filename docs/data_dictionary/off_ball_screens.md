# off_ball_screens

Screens set away from the ball to free a cutter, mirroring the structure of `picks` (screener, cutter, both defenders, defensive coverage on each, and outcomes for both players).

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`. `touchId` links to the cutter's touch, `scrTouchId` to the screener's touch. `cutterId`, `screenerId`, `cutterDefId`, `screenerDefId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the off ball screen. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `gameClock` | float | Game clock in seconds at the off ball screen. | No |
| `frame` | integer | Frame (at 25fps) since the start of the video of the off ball screen. | No |
| `wallClock` | integer | Time in ms between the off ball screen and the start of the video. | No |
| `direct` | boolean | 1 if cutter or screener shot, assist or is fouled directly after the screen. 0 otherwise. | No |
| `location` | list[float] | x, y coordinate of the screener. | No |
| `region` | string | Region of the screener. | No |
| `shotClock` | float | Number of seconds left on shot clock | No |
| `cutterId` | integer | SkillCorner Cutter Player ID. | No |
| `screenerId` | integer | SkillCorner Screener Player ID. | No |
| `cutterDefId` | integer | SkillCorner Player ID of the cutter's defender (the one before the screen if there's a switch). | No |
| `screenerDefId` | integer | SkillCorner Player ID of the screener's defender (the one before the screen if there's a switch). | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | No |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | No |
| `cutterDefType` | string | Defense type on cutter. One of none, trail, switch, whip, ride, top lock. | No |
| `screenerDefType` | string | Defense type on screener. One of none, switch, drop, show, jam. | No |
| `outcomes` | list[string] | List of actions involving the cutter following the screen, within the same chance. See outcomes definitions in touches. | No |
| `ledToTouch` | boolean | 1 if the cutter has a touch less than 4 seconds after the screen, 0 otherwise. | No |
| `ledToShot` | boolean | 1 if the cutter takes a shot less than 6 seconds after the screen, 0 otherwise. | No |
| `scrOutcomes` | list[string] | List of actions involving the screener following the pick, within the same chance. See outcomes definitions in touches. | No |
| `touchId` | string | SkillCorner Touch ID | No |
| `scrTouchId` | string | SkillCorner Screener Touch ID | No |
