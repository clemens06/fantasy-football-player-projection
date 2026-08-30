# MAE Results History

Mean absolute error in PPR Fantasy points, by prediction season

**Bolded = best model that season.**


### Original WR only model

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

### Initial WR + RB + TE model

*2020*
Linear Regression MAE: 33.74
Ridge Regression MAE: 34.24
Baseline MAE: 36.37
Random Forest MAE: 33.93
XGBoost MAE: 33.08
Ensemble MAE: **32.67**

*2021*
Linear Regression MAE: 36.3
Ridge Regression MAE: **31.93**
Baseline MAE: 32.61
Random Forest MAE: 32.99
XGBoost MAE: 32.52
Ensemble MAE: 33.09

*2022*
Linear Regression MAE: 31.54
Ridge Regression MAE: 28.85
Baseline MAE: **26.63**
Random Forest MAE: 29.1
XGBoost MAE: 30.17
Ensemble MAE: 30.18

*2023*
Linear Regression MAE: 28.98
Ridge Regression MAE: 28.83
Baseline MAE: 28.56
Random Forest MAE: 29.65
XGBoost MAE: 28.8
Ensemble MAE: **27.79**

*2024*
Linear Regression MAE: 31.19
Ridge Regression MAE: 31.2
Baseline MAE: 32.41
Random Forest MAE: 31.38
XGBoost MAE: **30.18**
Ensemble MAE: 30.6

Notes: Verified that there was some slight leakage causing significantly improved MAEs in this section. 

### Debugged and cleaned WR + RB + TE model Pre final model development
Predicting: 2020 | Position: WR
Training: (159, 21)
Testing: (169, 21)
Baseline MAE: 45.4
Linear Regression MAE: 48.63
Ridge Regression MAE: 47.81
Random Forest MAE: 46.89
XGBoost MAE: 46.12
Ensemble MAE: 46.27
Best model this season: Baseline (MAE: 45.4 )

Predicting: 2020 | Position: RB
Training: (107, 21)
Testing: (114, 21)
Baseline MAE: 55.76
Linear Regression MAE: 54.2
Ridge Regression MAE: 53.55
Random Forest MAE: 54.97
XGBoost MAE: 55.94
Ensemble MAE: 52.63
Best model this season: Ensemble (MAE: 52.63 )

Predicting: 2020 | Position: TE
Training: (91, 21)
Testing: (95, 21)
Baseline MAE: 36.37
Linear Regression MAE: 33.74
Ridge Regression MAE: 34.24
Random Forest MAE: 33.93
XGBoost MAE: 33.08
Ensemble MAE: 32.67
Best model this season: Ensemble (MAE: 32.67 )

Predicting: 2021 | Position: WR
Training: (328, 21)
Testing: (187, 21)
Baseline MAE: 47.54
Linear Regression MAE: 46.73
Ridge Regression MAE: 45.56
Random Forest MAE: 46.85
XGBoost MAE: 47.44
Ensemble MAE: 46.16
Best model this season: Ridge Regression (MAE: 45.56 )

Predicting: 2021 | Position: RB
Training: (221, 21)
Testing: (123, 21)
Baseline MAE: 49.78
Linear Regression MAE: 51.05
Ridge Regression MAE: 47.01
Random Forest MAE: 47.55
XGBoost MAE: 48.7
Ensemble MAE: 48.54
Best model this season: Ridge Regression (MAE: 47.01 )

Predicting: 2021 | Position: TE
Training: (186, 21)
Testing: (97, 21)
Baseline MAE: 32.61
Linear Regression MAE: 36.3
Ridge Regression MAE: 31.93
Random Forest MAE: 32.99
XGBoost MAE: 32.52
Ensemble MAE: 33.09
Best model this season: Ridge Regression (MAE: 31.93 )

Predicting: 2022 | Position: WR
Training: (515, 21)
Testing: (186, 21)
Baseline MAE: 40.73
Linear Regression MAE: 40.31
Ridge Regression MAE: 40.09
Random Forest MAE: 41.02
XGBoost MAE: 40.45
Ensemble MAE: 39.66
Best model this season: Ensemble (MAE: 39.66 )

Predicting: 2022 | Position: RB
Training: (344, 21)
Testing: (120, 21)
Baseline MAE: 51.15
Linear Regression MAE: 51.1
Ridge Regression MAE: 50.13
Random Forest MAE: 51.77
XGBoost MAE: 51.94
Ensemble MAE: 49.94
Best model this season: Ensemble (MAE: 49.94 )

Predicting: 2022 | Position: TE
Training: (283, 21)
Testing: (99, 21)
Baseline MAE: 26.63
Linear Regression MAE: 31.54
Ridge Regression MAE: 28.85
Random Forest MAE: 29.1
XGBoost MAE: 30.17
Ensemble MAE: 30.18
Best model this season: Baseline (MAE: 26.63 )

Predicting: 2023 | Position: WR
Training: (701, 21)
Testing: (167, 21)
Baseline MAE: 38.78
Linear Regression MAE: 40.9
Ridge Regression MAE: 40.52
Random Forest MAE: 40.29
XGBoost MAE: 39.11
Ensemble MAE: 39.42
Best model this season: Baseline (MAE: 38.78 )

Predicting: 2023 | Position: RB
Training: (464, 21)
Testing: (114, 21)
Baseline MAE: 54.89
Linear Regression MAE: 51.82
Ridge Regression MAE: 51.7
Random Forest MAE: 51.98
XGBoost MAE: 49.02
Ensemble MAE: 50.06
Best model this season: XGBoost (MAE: 49.02 )

Predicting: 2023 | Position: TE
Training: (382, 21)
Testing: (95, 21)
Baseline MAE: 28.56
Linear Regression MAE: 28.98
Ridge Regression MAE: 28.83
Random Forest MAE: 29.65
XGBoost MAE: 28.8
Ensemble MAE: 27.79
Best model this season: Ensemble (MAE: 27.79 )

Predicting: 2024 | Position: WR
Training: (868, 21)
Testing: (173, 21)
Baseline MAE: 48.1
Linear Regression MAE: 43.21
Ridge Regression MAE: 43.18
Random Forest MAE: 44.81
XGBoost MAE: 44.13
Ensemble MAE: 42.94
Best model this season: Ensemble (MAE: 42.94 )

Predicting: 2024 | Position: RB
Training: (578, 21)
Testing: (108, 21)
Baseline MAE: 49.07
Linear Regression MAE: 51.57
Ridge Regression MAE: 51.12
Random Forest MAE: 48.53
XGBoost MAE: 47.5
Ensemble MAE: 48.67
Best model this season: XGBoost (MAE: 47.5 )

Predicting: 2024 | Position: TE
Training: (477, 21)
Testing: (95, 21)
Baseline MAE: 32.41
Linear Regression MAE: 31.19
Ridge Regression MAE: 31.2
Random Forest MAE: 31.38
XGBoost MAE: 30.18
Ensemble MAE: 30.6
Best model this season: XGBoost (MAE: 30.18 )

Notes: Giant variance in MAE between positions, unlikely to be leakage though, because RB is so much higher than WR on average. TE is eyebrow-raisingly low, though...

# Feature Importance History

### Original WR only model > XGBoost

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

### Debugged and cleaned WR + RB + TE model Pre final model development > XGBoost

WR feature importance:
                     feature  importance
8    previous_fantasy_points    0.345076
2            receiving_yards    0.176738
12   fantasy_points_per_game    0.079194
1                 receptions    0.066666
6        receptions_per_game    0.042197
7   receiving_yards_per_game    0.033356
14              target_share    0.027196
0                    targets    0.026964
5           targets_per_game    0.026134
3              receiving_tds    0.023954
13                       age    0.018127
9                 catch_rate    0.016577
10          yards_per_target    0.016287
11       yards_per_reception    0.015079
17                   carries    0.014979
18    rushing_yards_per_game    0.014843
15             rushing_yards    0.013277
19      rushing_tds_per_game    0.012477
20          carries_per_game    0.012385
16               rushing_tds    0.009565

RB feature importance:
                     feature  importance
12   fantasy_points_per_game    0.255068
15             rushing_yards    0.163844
8    previous_fantasy_points    0.145921
1                 receptions    0.044989
2            receiving_yards    0.039622
14              target_share    0.031049
13                       age    0.028382
18    rushing_yards_per_game    0.027571
17                   carries    0.025507
7   receiving_yards_per_game    0.024174
6        receptions_per_game    0.024067
5           targets_per_game    0.024046
9                 catch_rate    0.021079
11       yards_per_reception    0.020858
20          carries_per_game    0.020337
4                      games    0.019549
19      rushing_tds_per_game    0.019541
10          yards_per_target    0.018933
3              receiving_tds    0.018053
16               rushing_tds    0.014853

TE feature importance:
                     feature  importance
8    previous_fantasy_points    0.234933
0                    targets    0.140943
2            receiving_yards    0.106733
12   fantasy_points_per_game    0.105958
14              target_share    0.063279
1                 receptions    0.044540
5           targets_per_game    0.040667
18    rushing_yards_per_game    0.034460
10          yards_per_target    0.031747
7   receiving_yards_per_game    0.030338
6        receptions_per_game    0.027178
17                   carries    0.025011
9                 catch_rate    0.021823
11       yards_per_reception    0.018362
20          carries_per_game    0.017790
13                       age    0.016404
15             rushing_yards    0.013899
4                      games    0.013016
3              receiving_tds    0.012917
16               rushing_tds    0.000000