# picks

On-ball screen (pick-and-roll / pick-and-pop) events: the ball handler, the screener, both of their defenders, the defensive coverage called on each (e.g. `ice`, `switch`, `blitz`, `drop`-equivalent `scrDefType` values), and the outcome for both players after the pick.

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`, `touchId`. `ballhandlerId`, `screenerId`, `ballhandlerDefId`, `screenerDefId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the pick. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | Yes |
| `gameClock` | float | Game clock in seconds at the pick. | No |
| `frame` | integer | Frame (at 25fps) since the start of the video of the pick. | No |
| `wallClock` | integer | Time in ms between the pick and the start of the video. | No |
| `direct` | boolean | 1 if ball handler or screener shot, assist or is fouled directly after the pick. 0 otherwise. | No |
| `location` | list[float] | x, y coordinate of the screener. | No |
| `region` | string | Region of the screener. | No |
| `shotClock` | float | Number of seconds left on shot clock | No |
| `ballhandlerId` | integer | SkillCorner Ball Handler Player ID. | No |
| `screenerId` | integer | SkillCorner Screener Player ID. | No |
| `ballhandlerDefId` | integer | SkillCorner Player ID of the ballhandler's defender (the one before the pick if there's a switch). | No |
| `screenerDefId` | integer | SkillCorner Player ID of the screener's defender (the one before the pick if there's a switch). | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | No |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | No |
| `locationType` | string | Locaiton type of the pick. Can be wing, middle, stepUp | No |
| `bhrDefType` | string | Defense type on ball handler. One of none, ice, switch, over, blitz, under. | No |
| `scrDefType` | string | Defense type on screener. One of none, ice, soft, switch, blitz, show. | No |
| `bhrOutcomes` | list[string] | List of actions involving the ball handler following the pick, within the same chance. See outcomes definitions in touches. | No |
| `scrOutcomes` | list[string] | List of actions involving the screener following the pick, within the same chance. See outcomes definitions in touches. | No |
| `handoffPick` | boolean | Boolean assessing if the event was a combination of a handoff and a pick | No |
| `touchId` | string | SkillCorner Touch ID | No |
