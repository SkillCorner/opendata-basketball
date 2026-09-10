# handoffs

Dribble hand-off events between a setter (who hands the ball off) and a receiver, mirroring the structure of `picks` (defensive coverage on each player, location type, whether it combined with a pick).

Join keys: `id` (primary key), `gameId`, `chanceId`, `possessionId`, `touchId`. `setterId`, `receiverId`, `setterDefId`, `receiverDefId` join to player ids in `game_data`.

| Field | Type | Definition | PBP derived |
|---|---|---|---|
| `id` | string | SkillCorner id of the handoff. | No |
| `gameId` | integer | SkillCorner Game ID. | Yes |
| `season` | string | Season depending on format of the competition, either {year} or {year}-{year+1} | Yes |
| `chanceId` | string | SkillCorner id of the associated chance. | No |
| `possessionId` | string | SkillCorner id of the associated possession. | No |
| `period` | integer | Number of the period (starts at 1 so the first quarter/period is 1). | No |
| `gameClock` | float | Game clock in seconds at the handoff. | No |
| `frame` | integer | Frame (at 25fps) since the start of the video of the handoff. | No |
| `wallClock` | integer | Time in ms between the handoff and the start of the video. | No |
| `direct` | boolean | 1 if receiver or setter shot, assist or is fouled directly after the handoff. 0 otherwise. | No |
| `location` | list[float] | x, y coordinate of the setter. | No |
| `region` | string | Region of the setter. | No |
| `shotClock` | float | Number of seconds left on shot clock | No |
| `receiverId` | integer | SkillCorner Receiver Player ID. | No |
| `setterId` | integer | SkillCorner Setter Player ID. | No |
| `receiverDefId` | integer | SkillCorner Player ID of the receiver's defender (the one before the handoff if there's a switch). | No |
| `setterDefId` | integer | SkillCorner Player ID of the setter's defender (the one before the handoff if there's a switch). | No |
| `offTeamId` | integer | SkillCorner Offensive Team ID. | No |
| `defTeamId` | integer | SkillCorner Defensive Team ID. | No |
| `locationType` | string | Locaiton type of the handoff. Can be wing, middle, stepUp | No |
| `receiverDefType` | string | Defense type on receiver. One of over, ice, under, switch. | No |
| `setterDefType` | string | Defense type on setter. One of none, ice, soft, switch. | No |
| `bhrOutcomes` | list[string] | List of actions involving the receiver following the handoff, within the same chance. See outcomes definitions in touches. | No |
| `handoffPick` | boolean | Boolean assessing if the event was a combination of a handoff and a pick | No |
| `touchId` | string | SkillCorner Touch ID | No |
