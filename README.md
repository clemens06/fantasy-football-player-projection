# Fantasy Football Projection Model

A fantasy points projection system built on NFL weekly stats (2018–2024), with an emphasis on **honest and leakage-free validation** over headline accuracy.

## What this does

Given a player's season-level stats, the model predicts that player's PPR fantasy points the following season. It's evaluated using walk-forward validation across five seasons (2020–2024), comparing five approaches against a simple "repeat last year's total" baseline.

## Data

- **Source:** [nflverse](https://github.com/nflverse/nflverse-data) weekly player stats and player biographical data, 2018–2024 regular seasons.
- **Scope:** Wide Receivers, Running Backs, Tight Ends, regular season games.
- **Unit of analysis:** one row per player-season, aggregated from weekly data and joined to team-level pass attempts to compute target share.

Players are identified by `player_id` (nflverse's `gsis_id`), not by name. Name-based joins can silently merge or split players who show up under different name formats across seasons or sources (e.g. "N.Dell" vs. "T.Dell" for Nathaniel "Tank" Dell). This project verifies identity resolution explicitly before trusting any aggregation.

## Features

- Volume: targets, receptions, receiving yards, receiving TDs, rushing yards, rushing tds, carries, games
- Rate/efficiency: targets/game, receptions/game, receiving yards/game, catch rate, yards/target, yards/reception, rushing yards/game, rushing tds/game, carries/game
- Opportunity share: target share (player targets ÷ team pass attempts)
- Continuity: previous season's fantasy points, fantasy points/game
- Context: age, age squared (creates parabola for model to train on rather than just a line), age curve (even more explicit age graph, peak around 27.5, taper off as players get older or younger), prime age bonus, post 30 decline

## Methodology

### Validation: walk-forward, not random split

A random train/test split would let the model train on some of a player's future outcomes while predicting others from the same season, which is not representative of how the model would actually be used (predicting a future season from past data only). So, instead, for each prediction year Y, the model trains only on rows where the outcome (next_season) is strictly before Y, and tests on rows where next_season == Y: 
train_df = model_df[model_df["next_season"] < prediction_season] 
test_df  = model_df[model_df["next_season"] == prediction_season]

An earlier iteration filtered training data by season < prediction_season rather than next_season < prediction_season. Because next_season = season + 1, that earlier version let the training set include the exact player-season rows used as the test set, so the model was trained on the answers it was then "predicting."

### Models compared

Six approaches are evaluated per season: Linear Regression, Ridge Regression, Random Forest, XGBoost, an unweighted average of Linear + XGBoost ("Ensemble"), and a naive baseline that simply repeats the player's prior-season point total.

### Development
This project went through several rounds of iteration before reaching the validated pipeline described above, starting with Wide Receivers only, then an early single-split baseline, tests of individual features in isolation, discovery and fix of validation leakage bugs, adding data, adding more position groups and applicable features, cluttering, and decluttering. I made my best attempt at recording data in testing.md, throwing ideas at the wall in todo.md, and keeping everything clean in the main nfl_analysis.py, because my goal in creating this project was to teach myself the skills required to build and use a model like this. I hope to one day look back at this model and laugh at how bad it was.

### SQL
The core pipeline uses pandas in this project, but a select few key aggregations were implemented in SQL against a local SQLite database to validate the pandas logic to get some hands-on SQL experience.
sql_queries.py loads the same CSVs into an SQLite database and reproduces two operations
- filtered aggregation: team pass attempts per week, computed with WHERE position = 'QB' and GROUP BY season, week, team. This matches the pandas groupby().sum() for building target_share
- join: player identity and biographical data merged onto weekly stats using LEFT JOIN ... ON weekly_stats.player_id = players.gsis_id, matching the pandas.merge() used to attach player age.


## Results

Check testing.md for most recent results on projections, MAEs, and feature importances, as well as notes and analysis.

## Repo structure

data/raw/           weekly stats CSVs (2018–2024) and player bio data
nfl_analysis.py         main pipeline: load > aggregate > feature engineer > validate > project > error-analyze