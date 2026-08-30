# MAE Results History

Mean absolute error in PPR Fantasy points, by prediction season

**Bolded = best model that season.**

### Original WR Baseline projections

*2024*
Linear Regression: 46.59
Random Forest: 49.13
Baseline : 51.54

Notes: Trained on 2021 > 2022 and 2022 > 2023, tested on 2023 > 2024. Only had volume features at the time.

### Completed WR only model

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

Notes: The Linear+XGBoost ensemble wins outright in 3 of 5 seasons; Ridge Regression wins the other 2. Between the two, one of them is the best or second-best performer in every season tested. Random Forest, the model this project started with, never wins a single season once evaluated head-to-head.

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

Initial note: Feature importance is model-specific, not a property of the data alone. It describes how a particular model used each feature, so it should come from a model that's actually part of the deployed pipeline. I actually used Random Forest for this early on, back when it was still assumed to be the best-performing model, but once the head-to-head validation showed otherwise, importance was recomputed from XGBoost, since XGBoost is one of the two models in the deployed ensemble. As the project develops further, this may shift away from XGBoost as well.

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

Initial analysis: previous fantasy points and receiving yards dominate, together accounting for over half the model's decision-making. This makes sense because this is largely a proxy for "how good was this player recently." Two differences from the earlier Random Forest ranking are worth noting: receptions ranks noticeably higher here (0.081 vs. 0.039 in RF), and age ranks noticeably lower (0.020 vs. 0.053). This leads me to believe that different model types can weigh the same features substantially differently even when trained on identical data. target share, added specifically to capture opportunity independent of pace/volume, landed in the middle of the pack and didn't meaningfully move validation MAE on its own, suggesting the model has probably hit a ceiling on what stat-based features can add.

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

Notes: I really want to switch this from XGBoost to an auto-selected model because this is pretty presumptive for now. Also, there are a lot of near-negligible features happening, and I think the high levels of redundancy I have included in my features has spurred that. We'll see!

# Projection History

### Debugged and cleaned WR + RB + TE model pre final model development
Top 10 WR Projections for 2025
     player_name  games  targets  receptions  receiving_yards  fantasy_points_ppr       age  projected_fantasy_points
   Ja'Marr Chase     17      175         127             1708              403.00 24.835044                275.433533
Justin Jefferson     17      154         103             1533              317.48 25.544148                274.811646
      Puka Nacua     11      106          79              990              206.60 23.592060                264.218689
Brian Thomas Jr.     17      133          87             1282              284.00 22.231348                263.394623
    Drake London     17      158         100             1271              280.80 23.438741                262.450439
     Tee Higgins     12      109          73              911              222.10 25.952088                245.815887
      A.J. Brown     13       97          67             1079              216.90 27.504449                244.695190
     CeeDee Lamb     15      152         101             1194              263.40 25.733060                243.011658
   Davante Adams     14      141          85             1063              241.30 32.019165                234.972305
   Ladd McConkey     16      112          82             1149              240.90 23.137577                227.379623

Top 10 RB Projections for 2025
player_name  games  targets  receptions  receiving_yards  fantasy_points_ppr       age  projected_fantasy_points
      Jahmyr Gibbs     17       63          52              517               362.9 22.784394                245.141296
       Chase Brown     16       65          54              360               255.0 24.780287                239.530273
     De'Von Achane     17       87          78              592               299.9 23.216975                231.351868
       Josh Jacobs     17       43          36              342               293.1 26.885695                223.897171
    Kyren Williams     16       40          34              182               272.1 24.347707                221.317490
        James Cook     16       38          32              258               266.7 25.267625                221.310104
       Breece Hall     16       76          57              483               240.9 23.586585                217.814499
Kenneth Walker III     11       53          46              299               181.2 24.197125                217.068863
      Alvin Kamara     14       89          68              543               265.3 29.437372                215.895416
         Joe Mixon     14       52          36              309               240.5 28.438056                215.797409

Top 10 TE Projections for 2025
  player_name  games  targets  receptions  receiving_yards  fantasy_points_ppr       age  projected_fantasy_points
 Trey McBride     16      147         111             1146               243.8 25.108830                186.707169
 Brock Bowers     17      153         112             1194               262.7 22.050650                180.943726
  Sam LaPorta     16       83          60              726               174.6 23.967146                175.692444
George Kittle     15       94          78             1106               236.6 31.227926                170.571930
  Jonnu Smith     17      111          88              884               222.3 29.360712                158.447586
   Cade Otton     14       87          59              600               140.6 25.713895                148.609238
 Tucker Kraft     17       70          50              707               163.3 24.158795                143.311371
   Kyle Pitts     17       74          47              602               131.2 24.235455                134.558624
  David Njoku     11       97          64              505               148.5 28.476386                133.231583
 Travis Kelce     16      133          97              823               195.4 35.238877                130.694077