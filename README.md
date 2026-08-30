# Fantasy Football WR Projection Model

A wide receiver fantasy points projection system built on NFL weekly stats (2018–2024), with an emphasis on **honest and leakage-free validation** over any single model's headline accuracy.

## What this does

Given a WR's season-level stats, the model predicts that player's PPR fantasy points the following season. It's evaluated using walk-forward validation across five seasons (2020–2024), comparing six approaches against a simple "repeat last year's total" baseline.

## Data

- **Source:** [nflverse](https://github.com/nflverse/nflverse-data) weekly player stats and player biographical data, 2018–2024 regular seasons.
- **Scope:** Wide receivers only (`position == "WR"`), regular season games (`season_type == "REG"`).
- **Unit of analysis:** one row per player-season, aggregated from weekly data and joined to team-level pass attempts to compute target share.

Players are identified by `player_id` (nflverse's `gsis_id`), not by name. Name-based joins can silently merge or split players who show up under different name formats across seasons or sources (e.g. "N.Dell" vs. "T.Dell" for Nathaniel "Tank" Dell) — this project verifies identity resolution explicitly before trusting any aggregation.

## Features

- Volume: targets, receptions, receiving yards, receiving TDs, games
- Rate/efficiency: targets/game, receptions/game, yards/game, catch rate, yards/target, yards/reception
- Opportunity share: target share (player targets ÷ team pass attempts)
- Continuity: previous season's fantasy points, fantasy points/game
- Context: age (at end of season)

## Methodology

### Validation: walk-forward, not random split

A random train/test split would let the model train on some of a player's future outcomes while predicting others from the same season, which is not representative of how the model would actually be used (predicting a future season from past data only). So, instead, for each prediction year Y, the model trains only on rows where the outcome (next_season) is strictly before Y, and tests on rows where next_season == Y: 
train_df = model_df[model_df["next_season"] < prediction_season] 
test_df  = model_df[model_df["next_season"] == prediction_season]

This obviously wasn't the first version of this code, an earlier iteration filtered training data by season < prediction_season rather than next_season < prediction_season. Because next_season = season + 1, that earlier version let the training set include the exact player-season rows used as the test set — the model was trained on the answers it was then "predicting." Catching and fixing this was one of the more important steps in this project; the corrected error numbers are what's reported below.

### Models compared

Six approaches are evaluated per season: Linear Regression, Ridge Regression, Random Forest, XGBoost, an unweighted average of Linear + XGBoost ("Ensemble"), and a naive baseline that simply repeats the player's prior-season point total.

### Development
This project went through several rounds of iteration before reaching the validated pipeline described above, including an early single-split baseline, tests of individual features in isolation, and discovery and fix of the validation leakage bug I described earlier. One notable early result was that adding previous-season fantasy points as a standalone feature improved Linear Regression MAE by only 0.02 points, while slightly hurting Random Forest. I found this to be an early signal that not every feature earns its place, which led me to more careful feature-by-feature testing used later in the project.

### SQL
The core pipeline uses pandas in this project, but a select few key aggregations were implemented in SQL against a local SQLite database to validate the pandas logic to get some hands-on SQL experience.
sql_queries.py loads the same CSVs into an SQLite database and reproduces two operations
- filtered aggregation: team pass attempts per week, computed with WHERE position = 'QB' and GROUP BY season, week, team. This matches the pandas groupby().sum() for building target_share
- join: player identity and biographical data merged onto weekly stats using LEFT JOIN ... ON weekly_stats.player_id = players.gsis_id, matching the pandas.merge() used to attach player age.


## Results

Most recent results posted here but I will keep a record of all results in testing.md

Mean absolute error in PPR Fantasy points, by prediction season:

**Bolded = best model that season.**

*2020*
Baseline: 45.40 
Linear: 46.00
Ridge: 46.28 
Random Forest: 46.54 
XGBoost: 46.28 
Ensemble: **45.18**

*2021*
Baseline: 47.54 
Linear: 45.99 
Ridge: **45.98** 
Random Forest: 47.27 
XGBoost: 47.85 
Ensemble: 46.33

*2022*
Baseline: 40.73 
Linear: 40.89 
Ridge: 40.50
Random Forest: 40.50
XGBoost: 40.17
Ensemble: **39.77**

*2023*
Baseline: 38.78
Linear: 38.78
Ridge: 39.02
Random Forest: 39.91
XGBoost: 38.12
Ensemble: **37.93**

*2024*
Baseline: 48.10
Linear: 42.40
Ridge: **42.36**
Random Forest: 44.52
XGBoost: 44.32
Ensemble: 42.71


The Linear+XGBoost ensemble wins outright in 3 of 5 seasons; Ridge Regression wins the other 2. Between the two, one of them is the best or second-best performer in every season tested. Random Forest, the model this project started with, never wins a single season once evaluated head-to-head.

### Analysis

The model does **not** consistently and dramatically beat "just predict last year's points again." In 2021 and 2023, no model beats the baseline by a meaningful margin. As far as I can tell, this is a real, well-documented property of WR fantasy production: year-to-year receiver output is generally volatile due to injuries, target competition, scheme changes, and quarterback play, and that volatility puts a ceiling on how far volume/efficiency stats alone can improve on recency. The model does, however, earn its keep in seasons like 2024, where it beats the baseline by nearly 6 points of MAE.

## Feature Importance (XGBoost)
Feature importance is model-specific, not a property of the data alone. It describes how a particular model used each feature, so it should come from a model that's actually part of the deployed pipeline. I actually used Random Forest for this early on, back when it was still assumed to be the best-performing model, but once the head-to-head validation above showed otherwise, importance was recomputed from XGBoost, since XGBoost is one of the two models in the deployed ensemble.

previous_fantasy_points    0.332
receiving_yards            0.211
fantasy_points_per_game    0.084
receptions                 0.081
receptions_per_game        0.047
yards_per_game             0.044
targets_per_game           0.032
targets                    0.030
target_share               0.029
receiving_tds              0.027
age                        0.020

previous fantasy points and receiving yards still dominate, together accounting for over half the model's decision-making. This makes sense because this is largely a proxy for "how good was this player recently." Two differences from the earlier Random Forest ranking are worth noting: receptions ranks noticeably higher here (0.081 vs. 0.039 in RF), and age ranks noticeably lower (0.020 vs. 0.053). This leads me to believe that different model types can weigh the same features substantially differently even when trained on identical data. target share, added specifically to capture opportunity independent of pace/volume, landed in the middle of the pack and didn't meaningfully move validation MAE on its own, suggesting the model has probably hit a ceiling on what stat-based features can add.

## What I would build next
- Team role/hierarchy features (WR1/2/3 on their team by targets) because exact numbers are probably less stable than role
- Uncertainty estimates on each projection (range rather than exact number)
- Add RB and TE
- Dynasty trade value tool built on these projections + an age curve rather than treating rankings as point values

## Repo structure

data/raw/           weekly stats CSVs (2018–2024) and player bio data
nfl_analysis.py         main pipeline: load > aggregate > feature engineer > validate > project > error-analyze