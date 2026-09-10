# Aggregate table column reference

Column reference for the three season-level aggregate files in `data/aggregates/`: `acb_shotsaggregates_20252026.csv`, `acb_drivesaggregates_20252026.csv`, `acb_picksaggregates_20252026.csv`. Each is a player-season roll-up, offense only, built from the `shots`, `drives` and `picks` Dynamic Events tables described in the [data dictionary](data_dictionary/README.md). See the [primer](PRIMER.md#how-the-season-aggregates-are-computed) for how these fit into the wider pipeline.

Every column family below has been checked against the published CSVs; column counts and bucket values are as delivered.

## Grain and identity columns (all three tables)

**Grain: one row per player, per team, per season.** A player who was traded mid-season gets one row per team they played for, PLUS an extra season-total row with `team_id` empty and `team_name` = `"total"` that aggregates across all their teams. Summing a metric column straight down the file double-counts anyone who has a total row — filter to either the per-team rows or the total rows before aggregating across players, don't mix both for the same player.

Row counts for ACB 2025-2026 (18 teams): `acb_shotsaggregates_20252026.csv` has 326 rows / 316 distinct players, `acb_drivesaggregates_20252026.csv` has 301 rows, `acb_picksaggregates_20252026.csv` has 319 rows. Row counts differ across the three files because a player only gets a row in a given file if they recorded at least one event of that type (e.g. a player with zero tracked picks has no row in the picks file).

Column order in the CSVs: `competition_id`, `competition_name`, `season_id`, `season_name`, `player_id`, `player_name`, `team_id`, `team_name`, `games_played`, then the metric columns verbatim from the pipeline (families documented per table below).

| Column | Type | Definition |
|---|---|---|
| `competition_id` | INT64 | Competition (league) identifier. |
| `competition_name` | STRING | Competition (league) display name, e.g. 'ACB'. |
| `season_id` | INT64 | Season identifier. |
| `season_name` | STRING | Season label formatted as 'start_year-end_year', e.g. '2025-2026'. |
| `player_id` | INT64 | Player identifier (integer SkillCorner player id), joins to `game_data` player ids. |
| `player_name` | STRING | Player display name. |
| `team_id` | INT64 | Team the row belongs to. Empty marks the all-teams season TOTAL row for a player who changed teams mid-season (see grain note above). |
| `team_name` | STRING | Team display name. `'total'` on the all-teams season row. |
| `games_played` | INT64 | Number of games in which the player was on court for at least one chance (derived from `chance_players`, split by team). This is on-court presence only — it is **not** a count of games with a tracked shot, drive or pick, so a player can have `games_played > 0` with zero attempts in that same aggregate row. 293 of the 327 games of the 2025-2026 season (regular season and playoffs) are included in the source data; the missing games are mostly the playoffs plus a few regular-season fixtures, so `games_played` tops out at whatever number of those 293 games that player's team is covered for (teams range from 31 to 34 games in the 293-game set). |
| `possessions_played` | INT64 | Offensive possessions the player was on court for (on-court presence, not possessions with a tracked event). Counts a player on court at any point in the possession, so mid-possession substitutions push this ~3% above 5 × possessions — it will not reconcile against a team-level total. |

## shots aggregates (`acb_shotsaggregates_20252026.csv`)

Player-season shot attempts, makes and points, pivoted by court zone, contest level, and shot type. Every count/rate below is offense — a player's own shooting.

* **Totals** — `attempts`, `made_baskets` (renamed `mades` in some columns), `total_points`/`points`, `assisted_mades` (makes assisted by a teammate), `blocked_on_attempts`, `fouled_fg_attempts`/`fouled_fg_mades` (and-ones), `avg_attempts_distance` (average feet to the hoop across attempts). `attempts` follows FIBA box-score convention and **excludes field goal attempts missed while the shooter was fouled** (these are scored as free throw trips, not field goal attempts) — the underlying `shots` event table is broader and includes those events (41,684 shot events vs. 38,029 `attempts` league-wide in ACB 2025-2026), so don't expect `attempts` to reconcile against a raw count of `shots` rows. `total_points` includes free throw points scored on and-one plays (a made basket plus a made bonus free throw), so it is not simply `2 × fg2_mades + 3 × fg3_mades`.
* **Derived rates** — `fg_percentage`, `efg_percentage` (effective FG%, weights 3s at 1.5x), `points_per_shot`.
* **By contest level** (`cl_*`, 5 buckets × 7 metrics = 35 columns) — `cl_open_*`, `cl_light_*`, `cl_average_*`, `cl_plus_*`, `cl_blocked_*`, each with `_attempts`, `_mades`, `_misses`, `_attempt_rate`, `_fg_percentage`, `_points_per_shot`, `_total_points`. Matches the `contestLevel` values on the `shots` event table: open, light, average, plus, blocked.
* **By court zone** (`zone_*`, 71 columns) — `_attempts`/`_mades`/`_misses`/`_total_points` per zone, plus `_attempt_rate`/`_fg_percentage`/`_points_per_shot` for the split 3-point zones. Two-point zones: `restricted_area`, `paint_non_ra` (paint outside the restricted area), `mid_range`. Three-point zones: `corner_3` (also split into `corner_3_left` / `corner_3_right`), `wing_3_left` / `wing_3_right`, `top_3`, `above_break_3` (wings + top combined), and `three` (all 3-point attempts, with `_attempt_rate` / `_fg_percentage`). Catch-all zones: `backcourt`, `far`, `other`. This zone vocabulary is coarser than the `region` strings on the event tables (see [data dictionary README](data_dictionary/README.md#markings--coordinate-system)).
* **By zone family** (12 columns) — three two-point families with `_attempts`/`_mades`/`_fg_percentage`/`_attempt_rate`: `rim` (= `zone_restricted_area_*`), `short_midrange_paint` (= `zone_paint_non_ra_*`), `long_midrange` (= `zone_mid_range_*`). Three-point attempts and the `backcourt`/`far`/`other` zones belong to no family, so the three families sum to slightly less than `two_attempts`.
* **By shot type** (`cst_*`, complex shot type, 98 columns) — 14 shot types × 7 metrics: `catch_and_shoot`, `dribble_pull_up`, `dunk`, `floater`, `heave`, `hook`, `layup`, `leaner`, `lob`, `off_move`, `post_fadeaway`, `shake_and_raise`, `stepback`, `tip`. Matches `complexShotType` on the `shots` event table.
* **Catch-and-shoot / off-dribble** (`cns_*` / `od_*`, 30 columns) — a coarser 2-way split (catch-and-shoot vs. off-the-dribble) than the full shot-type breakdown, each with `_attempts`, `_mades`, `_fg_percentage`, `_efg_percentage`, `_points_per_shot`, `_total_points`, plus a 2pt/3pt split (`_two_*`, `_three_*`) and free throws drawn on that shot type (`_ft_attempts`, `_ft_mades`). Matches the `catchAndShoot` boolean on the `shots` event table (catch-and-shoot = release ≤ 1.5s or `complexShotType = catchAndShoot`).
* **Contested / uncontested** (30 columns, same shape as catch-and-shoot / off-dribble) — a coarser 2-way split of contest level than the 5-bucket `cl_*` breakdown. Matches the `contested` boolean on the `shots` event table (contested = `contestLevel` in average/plus/blocked).

## drives aggregates (`acb_drivesaggregates_20252026.csv`)

Player-season drive volume and outcomes, pivoted by how the drive started, how it ended, its direction and its origin court zone.

* **Totals** (16 columns) — `total_drives`, `successful_drives` / `unsuccessful_drives` (successful = basket made, assist, or foul drawn), `made_baskets`, `assists` (drive led to a teammate scoring off the ball handler's pass), `potential_assists` (pass could have led to a score but was missed/turned over), `fouls` (drew a shooting/non-shooting foul), `fga_in_drive`, `field_points_in_drive`, `ft_attempts_in_drive`/`ft_mades_in_drive`, `points` (own FG points + assisted FG points, excludes free throws), `points_per_shot_in_drive`.
* **Derived rates** — the totals above as a share of `total_drives`: `successful_drives_rate`, `unsuccessful_drives_rate`, `made_baskets_rate`, `assists_rate`, `potential_assists_rate`, `fouls_rate`, `points_per_drive`.
* **By play category** (`category_*`, 12 columns) — how the drive was created: `pick`, `handoff`, `off_ball_screen`, `iso`, `closeout`, `miscellaneous` (doesn't fit the other tracked origins). Each with `_count` and `_rate`. Matches the `category` field on the `drives` event table.
* **By end type** (`end_type_*`, 14 columns) — how the drive ended: `kickout` (pass out), `pullout` (reset without continuing), `pullup` (pull-up jumper), `interior_pass`, `shot_near_basket`, `turnover`, `stoppage` (whistle/dead ball, no other end type). Each with `_count` and `_rate`. Matches `endType` on the `drives` event table.
* **By direction** (4 columns) — `direction_left_*` / `direction_right_*` (which way the ball handler drove), count and rate.
* **By court zone** (6 columns) — origin zone of the drive, limited to `above_break_3`, `corner_3`, `mid_range` in the sample schema (drives don't usually originate in the restricted area/paint by definition, so rim-adjacent zones are not broken out here).
* **Drive type** — `blowby_count`/`blowby_rate` (defender beaten on the drive), `dribble_through_count`/`dribble_through_rate` (drove all the way through the paint), `direct_drives_count` (drive classified as ending directly in a shot/foul/turnover, vs. an indirect drive that reset into something else).

## picks aggregates (`acb_picksaggregates_20252026.csv`)

Player-season pick-and-roll production, tracked separately for each of the two roles a player can occupy on a pick: **ball-handler** (`handler_*` columns) and **screener** (`screener_*` columns). Every metric exists once per role, and is further split by defensive coverage and by screen location — this is the largest of the three files by column count (684 in the full offense schema).

**Direct picks only.** The picks aggregates count only picks where the raw event's `direct` field is true (the ball handler or screener shot, was assisted, or was fouled directly after the pick — see `direct` on the [`picks`](data_dictionary/picks.md) event table). In ACB 2025-2026 that's 22,080 of 42,156 total pick events (~52%). Counting rows in the raw `picks` event table therefore gives roughly double `handler_total_picks`; filter on `direct = true` before comparing raw event counts to these aggregates.

* **Shared identity/totals** — the common identity block plus `possessions_played`, `team_id`, `team_name` (one set, not duplicated per role).
* **Role totals** (`handler_*` / `screener_*`, 35 columns per role) — `_total_picks`, `_successful_pick` / `_unsuccessful_pick` (successful = score, assist, or foul drawn), `_score` (own make, split `_score_2pt`/`_score_3pt`), `_miss` (own miss, split 2pt/3pt), `_assist` (assisted a teammate, split `_to_screener` vs `_to_other`), `_assist_opportunity` (pass created a scoring chance whether converted or not, same to_screener/to_other split), `_pass` (split `_pass_to_screener`/`_pass_to_other`), `_only_pass_pick` (passed with no shot/assist), `_no_outcome_pick`, `_turnover`, `_foul` (drew a foul), `_block` (shot blocked), `_shot_taken`, `_fga_in_pick`, `_field_points_in_pick`, `_ft_attempts_in_pick`/`_ft_mades_in_pick`, `_points`, `_points_per_shot_in_pick`, `_ppp` (points per pick).
* **Role derived rates** (20-21 columns per role) — the totals above as a share of `_total_picks` (`_pct` or `_rate` suffix; both are used inconsistently in the schema — treat them as synonyms), plus `_fg2_pct` / `_fg3_pct` (make percentage conditional on a 2pt/3pt attempt being taken, not a share of total picks).
* **By defensive coverage** (`_vs_<coverage>`, 245 columns per role) — every role-totals and role-derived-rate metric repeated once per defensive coverage the player faced. Ball-handler buckets (`handler_*_vs_*`, matching `bhrDefType` on the `picks` event table): `blitz`, `ice`, `over`, `switch`, `under`. Screener buckets (`screener_*_vs_*`, matching `scrDefType`): `blitz`, `ice`, `show`, `soft`, `switch`. The two vocabularies differ by role; picks with no coverage called (`none`) are counted in the role totals but have no `_vs_` bucket of their own.
* **By screen location** (`_at_<location>`, 36 columns per role) — every role metric repeated once per pick location: `middle`, `stepUp`, `wing`, `unknown` (unclassified). Matches `locationType` on the `picks` event table.

**Always empty in this release** — five columns are 100% null across all of ACB 2025-2026 (no player recorded an event in the `unknown`-location bucket combined with these particular metrics): `handler_fg2_pct_vs_blitz`, `handler_ppp_at_unknown`, `handler_score_rate_at_unknown`, `screener_ppp_at_unknown`, `screener_score_rate_at_unknown`. Don't treat a null in these five as missing data — it reflects zero underlying events for that combination.

## Notes on reading these columns

* `_rate` and `_pct` columns are always a share of that role's `_total_picks` / `total_drives` / shot attempts within the same pivot bucket (e.g. `handler_score_rate_at_middle` divides by `handler_picks_at_middle`, not by the player's overall `handler_total_picks`) — read the bucket suffix carefully before comparing rates across buckets.
* `points` on `drives` and `picks` excludes free throw points; free throws are broken out separately (`ft_attempts_in_drive`/`ft_mades_in_drive`, `_ft_attempts_in_pick`/`_ft_mades_in_pick`).
* A player with a `team_id` of NULL and `team_name` of `'total'` is the season-total row for a player who changed teams mid-season; don't double count them against their per-team rows.
