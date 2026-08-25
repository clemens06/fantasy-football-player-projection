# Project Log

NOTE: results here predate the leakage-bug fix and the extended 2018–2024 dataset. See README for current validated results

## Experiment 1 — Baseline WR projection model

### Goals
Predict a WR's next-season PPR fantasy points using their previous-season performance.

### Data
- NFL weekly player statistics
- Seasons: 2021–2024
- Position: WR
- 150 columns in raw dataset
- 75,000+ rows per season

### Data processing
Converted weekly WR statistics into season-level player statistics.

Features:
- targets
- receptions
- receiving yards
- receiving touchdowns
- games played
- targets per game
- receptions per game
- yards per game

Target:
- next-season PPR fantasy points

### Train/test split
Training:
- 2021 → 2022
- 2022 → 2023
- 355 player-seasons

Testing:
- 2023 → 2024
- 177 player-seasons

### Results

Linear Regression:
- MAE: 46.29

Random Forest:
- MAE: 48.83

### Conclusion
Linear Regression performed better than Random Forest in the baseline experiment.

### Next experiment
Add previous-season PPR fantasy points as a feature and determine whether prediction accuracy improves.

### Results
Adding previous-season PPR fantasy points reduced Linear Regression MAE from 46.2946 to 46.2713, an improvement of only 0.0233 points. Random Forest performance worsened slightly from 48.8289 to 48.9223. Previous-season PPR therefore provides very little additional predictive value given the existing features.

### Baseline addition and comparison

Linear Regression MAE: 46.59
Random Forest MAE: 49.13
Naive Baseline MAE: 51.54

Linear Regression performed best and improved MAE by around 9.6% compared with simply using the previous season's fantasy points.
Random Forest performed worse than Linear Regression.