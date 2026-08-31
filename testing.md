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

### Final WR + RB + TE model pre XGBoost tuning experimentation
    season position  linear_mae  ridge_mae  baseline_mae  random_forest_mae  xgboost_mae  ensemble_mae     best_model   best_mae
0     2020       WR   49.604254  48.019791     45.403905          46.800519    46.653796     46.913399       Baseline  45.403905
1     2020       RB   55.605055  53.518050     55.762281          55.066591    54.604642     52.937667       Ensemble  52.937667
2     2020       TE   34.595364  34.223247     36.367368          33.856725    33.367862     32.787292       Ensemble  32.787292
3     2021       WR   46.240402  46.111259     47.539144          46.406968    46.922000     45.443553       Ensemble  45.443553
4     2021       RB   51.715816  48.512364     49.783415          48.412203    48.909700     48.610417  Random Forest  48.412203
5     2021       TE   37.918337  32.858874     32.614227          32.552982    32.839628     34.446079  Random Forest  32.552982
6     2022       WR   41.318066  40.690437     40.732366          40.125708    39.627826     39.612640       Ensemble  39.612640
7     2022       RB   51.325907  50.308100     51.147667          51.773021    51.358877     49.488339       Ensemble  49.488339
8     2022       TE   31.714421  28.976261     26.632121          29.189591    30.198041     30.124323       Baseline  26.632121
9     2023       WR   40.037082  39.552255     38.779521          39.102153    38.725367     38.602560       Ensemble  38.602560
10    2023       RB   51.894595  51.565047     54.893684          50.433916    47.810402     49.013085        XGBoost  47.810402
11    2023       TE   30.115058  29.549170     28.555579          29.338762    29.021176     28.211070       Ensemble  28.211070
12    2024       WR   42.952164  43.088732     48.095607          43.629428    44.295629     42.793026       Ensemble  42.793026
13    2024       RB   52.286312  51.942118     49.070185          46.425231    46.044560     48.503517        XGBoost  46.044560
14    2024       TE   31.065786  30.717415     32.407158          31.480033    29.604682     29.910521        XGBoost  29.604682

Average best MAE by position:
position
TE    29.957630
WR    42.371137
RB    48.938634

OVERALL BEST MODEL
Best model by average MAE: ensemble_mae
Average MAE:         41.16
linear_mae           43.226
ridge_mae            41.976
baseline_mae         42.519
random_forest_mae    41.640
xgboost_mae          41.332
ensemble_mae         41.160

Notes: Apologies for the formattings inconsistencies. This section is much better organized and readable so will stick with this from here. No major differences from previous section, tight end still concerns me but as of now haven't found whatever problem there may be.

### FINAL FINAL WR + RB TE model


    season position  linear_mae  ridge_mae  baseline_mae  random_forest_mae  xgboost_mae  ensemble_mae best_model   best_mae
0     2020       WR   49.604254  48.019791     45.403905          46.800519    46.230264     46.513892   Baseline  45.403905
1     2020       RB   55.605055  53.518050     55.762281          55.066591    53.514429     51.260676   Ensemble  51.260676
2     2020       TE   34.595364  34.223247     36.367368          33.856725    33.367862     32.787292   Ensemble  32.787292
3     2021       WR   46.240402  46.111259     47.539144          46.406968    46.773460     45.561395   Ensemble  45.561395
4     2021       RB   51.715816  48.512364     49.783415          48.412203    47.089194     47.619270    XGBoost  47.089194
5     2021       TE   37.918337  32.858874     32.614227          32.552982    32.312382     33.787647    XGBoost  32.312382
6     2022       WR   41.318066  40.690437     40.732366          40.125708    38.230013     38.563552    XGBoost  38.230013
7     2022       RB   51.325907  50.308100     51.147667          51.773021    48.257496     48.713047    XGBoost  48.257496
8     2022       TE   31.714421  28.976261     26.632121          29.189591    28.634698     29.668113   Baseline  26.632121
9     2023       WR   40.037082  39.552255     38.779521          39.102153    37.124396     37.846787    XGBoost  37.124396
10    2023       RB   51.894595  51.565047     54.893684          50.433916    46.257852     48.260625    XGBoost  46.257852
11    2023       TE   30.115058  29.549170     28.555579          29.338762    27.729491     28.285886    XGBoost  27.729491
12    2024       WR   42.952164  43.088732     48.095607          43.629428    43.678498     42.586953   Ensemble  42.586953
13    2024       RB   52.286312  51.942118     49.070185          46.425231    43.953228     47.285598    XGBoost  43.953228
14    2024       TE   31.065786  30.717415     32.407158          31.480033    29.474697     29.812345    XGBoost  29.474697

Average best MAE by position:
position
TE    29.787197
WR    41.781333
RB    47.363689

Best model by average MAE: xgboost_mae
Average MAE: 40.18
linear_mae           43.226
ridge_mae            41.976
baseline_mae         42.519
random_forest_mae    41.640
xgboost_mae          40.175
ensemble_mae         40.570

Notes: Tuning had a HUGE EFFECT ON MAES!!!!! XGBoost and Ensemble now win 14 out of 15 times, the only loss coming to Baseline in 2022 on TEs, where XGBoost still came in second. The best model is now officially XGBoost, cutting its MAE down by a full point from the previous results. 

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

### Final WR + RB + TE model pre XGBoost tuning experimentation

WR feature importance:
                 feature  importance
 previous_fantasy_points    0.268278
         receiving_yards    0.171867
              receptions    0.124114
 fantasy_points_per_game    0.088632
     receptions_per_game    0.029588
receiving_yards_per_game    0.029016
        targets_per_game    0.026607
            prev_2yr_avg    0.023161
            target_share    0.021400
                 targets    0.020139
           receiving_tds    0.018141
                     age    0.017455
              catch_rate    0.015956
   fantasy_points_change    0.015845
         post_30_decline    0.014985
    rushing_tds_per_game    0.013762
     yards_per_reception    0.013368
  rushing_yards_per_game    0.013027
        yards_per_target    0.012975
        carries_per_game    0.011949

RB feature importance:
                 feature  importance
 fantasy_points_per_game    0.265248
 previous_fantasy_points    0.133970
           rushing_yards    0.107215
              receptions    0.037295
         receiving_yards    0.034383
  rushing_yards_per_game    0.029863
            target_share    0.027190
             rushing_tds    0.025242
        targets_per_game    0.024572
                 carries    0.024013
                     age    0.024007
            prev_2yr_avg    0.023713
         post_30_decline    0.023230
   fantasy_points_change    0.021668
                   games    0.021074
     receptions_per_game    0.020823
        yards_per_target    0.019561
               age_curve    0.019395
        carries_per_game    0.019279
receiving_yards_per_game    0.019123

TE feature importance:
                 feature  importance
 previous_fantasy_points    0.190684
        targets_per_game    0.145299
         receiving_yards    0.111058
                 targets    0.109881
 fantasy_points_per_game    0.081043
            target_share    0.042446
              receptions    0.032723
        carries_per_game    0.029770
receiving_yards_per_game    0.029436
           rushing_yards    0.024493
            prev_2yr_avg    0.023642
  rushing_yards_per_game    0.023275
        yards_per_target    0.022398
     yards_per_reception    0.016504
                 carries    0.016307
                   games    0.016296
              catch_rate    0.016171
                     age    0.015521
           receiving_tds    0.015446
   fantasy_points_change    0.014511

Notes: Same as before honestly. I should investigate the discrepancies between importance in features such as fantasy points per game and previous fantasy points between positions, since those are all very high importance features.

### FINAL FINAL WR + RB + TE model

WR feature importance:
                 feature  importance
 previous_fantasy_points    0.270523
         receiving_yards    0.256169
              receptions    0.050756
            prev_2yr_avg    0.029608
        targets_per_game    0.027298
receiving_yards_per_game    0.025420
           receiving_tds    0.024926
 fantasy_points_per_game    0.024400
         post_30_decline    0.022834
   fantasy_points_change    0.022096
                     age    0.021971
            target_share    0.020570
     receptions_per_game    0.018697
              catch_rate    0.018508
        carries_per_game    0.017784
    rushing_tds_per_game    0.016683
  rushing_yards_per_game    0.015653
     yards_per_reception    0.015401
             rushing_tds    0.014659
               age_curve    0.014223

RB feature importance:
                 feature  importance
 fantasy_points_per_game    0.185196
           rushing_yards    0.177952
 previous_fantasy_points    0.112888
         receiving_yards    0.047366
                 targets    0.032772
              receptions    0.032283
receiving_yards_per_game    0.030645
            target_share    0.030572
                 carries    0.029197
                     age    0.028542
        yards_per_target    0.028331
        targets_per_game    0.026692
  rushing_yards_per_game    0.024837
   fantasy_points_change    0.023323
              catch_rate    0.022996
             rushing_tds    0.020590
            prev_2yr_avg    0.020457
        carries_per_game    0.020102
               age_curve    0.019895
                   games    0.019254

TE feature importance:
                 feature  importance
                 targets    0.186112
 previous_fantasy_points    0.151175
 fantasy_points_per_game    0.111144
        targets_per_game    0.102255
         receiving_yards    0.075610
receiving_yards_per_game    0.058897
            target_share    0.054504
            prev_2yr_avg    0.032780
        yards_per_target    0.028245
           rushing_yards    0.023711
              catch_rate    0.023034
  rushing_yards_per_game    0.021885
              receptions    0.019740
                 carries    0.016973
     receptions_per_game    0.015587
               age_curve    0.015571
                   games    0.014791
     yards_per_reception    0.013897
                     age    0.012073
   fantasy_points_change    0.011303
   
Notes: Huge changes to all positions. Top to bottom, the model appears to be favoring age features to a greater extent than it did before. For TEs, Targets becomes the first volume stat to appear at the top of one of these lists. For RBs, top-end features' percentages seem to have dropped to favor volume stats, in particular rushing yards. WRs didn't have the same top-end features dropping, but receiving yards importance was bumped up by 8 percentage points.

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

Notes: I believe that in general these projections are skewing lower than they should be, especially when it comes to running backs. Keep in mind these projections are for the 2025 season (last year at the time of writing this). That said, these are by far the most fathomable projections that the model has produced thus far. All quality players (Even Kyle Pitts) that have legitimate fantasy upside. 
Some notable exclusions that I would like to investigate: No Saquon Barkley after a 2000 yard, 360ish point season in the top 10 is deeply disturbing, as well as no Bijan Robinson in spite of Gibbs being the #1 RB, no Derrick Henry (Though I suspect it's age playing a major factor for him, given the model doesn't know how to account for unicorn longevity), no hyper-consistent Amon-Ra St Brown, no Malik Nabers after a nuclear rookie season, and there might be some TEs I'm forgetting. 

### Final WR + RB + TE model pre XGBoost tuning experimentation

Top 20 WR Projections for 2025
        player_name  games  targets  receptions  receiving_yards  fantasy_points_ppr       age  projected_fantasy_points
   Justin Jefferson     17      154         103             1533              317.48 25.544148                251.698074
      Ja'Marr Chase     17      175         127             1708              403.00 24.835044                242.588943
   Brian Thomas Jr.     17      133          87             1282              284.00 22.231348                239.644180
       Drake London     17      158         100             1271              280.80 23.438741                229.553696
      Ladd McConkey     16      112          82             1149              240.90 23.137577                228.451782
 Jaxon Smith-Njigba     17      137         100             1130              253.00 22.877481                227.196030
        Tee Higgins     12      109          73              911              222.10 25.952088                227.123322
        CeeDee Lamb     15      152         101             1194              263.40 25.733060                222.337494
  Amon-Ra St. Brown     17      141         115             1263              316.18 25.188227                221.796951
     Jordan Addison     15       99          63              875              212.50 22.926762                219.452728
         A.J. Brown     13       97          67             1079              216.90 27.504449                219.281113
         Puka Nacua     11      106          79              990              206.60 23.592060                217.592514
       Nico Collins     12       99          68             1006              210.60 25.787817                207.907974
       Malik Nabers     15      170         109             1204              273.60 21.429158                206.586685
Marvin Harrison Jr.     17      116          62              885              196.50 22.390144                205.628372
   Jameson Williams     15       91          58             1001              212.20 23.767283                201.942413
     Garrett Wilson     17      154         101             1104              251.90 24.443532                201.652420
      Davante Adams     14      141          85             1063              241.30 32.019165                201.035950
      DeVonta Smith     13       89          68              833              199.40 26.130048                198.585556
     Jauan Jennings     15      113          77              975              210.50 27.477070                197.737732

Top 20 RB Projections for 2025
       player_name  games  targets  carries  rushing_yards  fantasy_points_ppr       age  projected_fantasy_points
      Jahmyr Gibbs     17       63      250           1412              362.90 22.784394                248.082718
       Chase Brown     16       65      229            990              255.00 24.780287                243.126160
     De'Von Achane     17       87      203            907              299.90 23.216975                242.012054
    Kyren Williams     16       40      316           1299              272.10 24.347707                238.535248
        James Cook     16       38      207           1009              266.70 25.267625                237.330124
      Alvin Kamara     14       89      228            950              265.30 29.437372                235.716141
   Jonathan Taylor     14       31      303           1431              244.70 25.949350                228.318314
    Bijan Robinson     17       72      304           1456              341.70 22.918549                228.215332
      James Conner     16       55      236           1094              253.80 29.659138                227.495575
       Josh Jacobs     17       43      301           1329              293.10 26.885695                221.311646
       Breece Hall     16       76      209            876              240.90 23.586585                216.941254
     Chuba Hubbard     15       54      250           1195              241.60 25.557837                216.564041
      Bucky Irving     17       52      207           1122              244.40 22.368241                214.153397
         Joe Mixon     14       52      245           1016              240.50 28.438056                213.904877
Kenneth Walker III     11       53      153            573              181.20 24.197125                213.257050
      J.K. Dobbins     13       38      195            905              191.80 26.039699                192.356491
     Derrick Henry     17       22      325           1921              336.40 30.989733                189.519684
  David Montgomery     14       38      185            775              221.72 27.567420                189.162842
       Aaron Jones     17       62      255           1138              241.60 30.080767                188.427856
    Saquon Barkley     16       43      345           2005              355.30 27.890486                186.680817

Top 20 TE Projections for 2025
   player_name  games  targets  receptions  receiving_yards  fantasy_points_ppr       age  projected_fantasy_points
  Brock Bowers     17      153         112             1194               262.7 22.050650                200.567825
   Sam LaPorta     16       83          60              726               174.6 23.967146                177.948547
  Trey McBride     16      147         111             1146               243.8 25.108830                177.450256
 George Kittle     15       94          78             1106               236.6 31.227926                175.999374
   Jonnu Smith     17      111          88              884               222.3 29.360712                166.600311
  Tucker Kraft     17       70          50              707               163.3 24.158795                140.523651
    Cade Otton     14       87          59              600               140.6 25.713895                124.133263
    Kyle Pitts     17       74          47              602               131.2 24.235455                123.951538
Pat Freiermuth     17       78          65              653               170.3 26.184805                120.829964
  Mark Andrews     17       69          55              673               188.8 29.319644                120.651009
  Travis Kelce     16      133          97              823               195.4 35.238877                114.072823
  Mike Gesicki     16       83          65              665               141.5 29.245722                109.138313
     Zach Ertz     17       91          66              654               177.4 34.140999                107.323540
  Hunter Henry     16       97          66              674               145.4 30.067077                106.843742
  Chig Okonkwo     16       70          52              479               113.6 25.314168                103.233177
     Noah Gray     16       49          40              437               113.3 25.672827                 99.236000
   David Njoku     11       97          64              505               148.5 28.476386                 96.172234
 Juwan Johnson     15       66          50              548               122.8 28.298426                 95.594429
Dalton Kincaid     13       75          44              448               100.8 25.204654                 94.766457
 Isaiah Likely     15       58          42              477               123.7 24.703628                 89.938690

Notes: Moved to top 20 to get a better picture. These rankings generally feels like a substantial improvement. Addition and improvement of age features do a better job of rewarding consistency while recognizing the possibility of young players having breakout seasons, which can be seen in players like Bijan Robinson, Brock Bowers, Brian Thomas Jr., and Jahmyr Gibbs having high predictions.

### FINAL FINAL WR + RB + TE model

Top 20 WR Projections for 2025
        player_name  games  targets  receptions  receiving_yards  fantasy_points_ppr       age  projected_fantasy_points
   Justin Jefferson     17      154         103             1533              317.48 25.544148                269.051697
   Brian Thomas Jr.     17      133          87             1282              284.00 22.231348                249.782776
      Ja'Marr Chase     17      175         127             1708              403.00 24.835044                247.929794
      Ladd McConkey     16      112          82             1149              240.90 23.137577                242.723099
         Puka Nacua     11      106          79              990              206.60 23.592060                242.370117
 Jaxon Smith-Njigba     17      137         100             1130              253.00 22.877481                241.645584
       Drake London     17      158         100             1271              280.80 23.438741                241.094131
        CeeDee Lamb     15      152         101             1194              263.40 25.733060                233.331192
     Jordan Addison     15       99          63              875              212.50 22.926762                225.483093
        Tee Higgins     12      109          73              911              222.10 25.952088                224.914459
  Amon-Ra St. Brown     17      141         115             1263              316.18 25.188227                221.891174
         A.J. Brown     13       97          67             1079              216.90 27.504449                216.742264
      Davante Adams     14      141          85             1063              241.30 32.019165                215.604568
Marvin Harrison Jr.     17      116          62              885              196.50 22.390144                204.327866
   Jameson Williams     15       91          58             1001              212.20 23.767283                204.118774
       Nico Collins     12       99          68             1006              210.60 25.787817                204.095093
        Jerry Jeudy     17      145          90             1229              240.90 25.689254                202.473297
      DeVonta Smith     13       89          68              833              199.40 26.130048                201.638916
     Jauan Jennings     15      113          77              975              210.50 27.477070                198.335266
     Garrett Wilson     17      154         101             1104              251.90 24.443532                193.527054

Top 20 RB Projections for 2025
       player_name  games  targets  carries  rushing_yards  fantasy_points_ppr       age  projected_fantasy_points
      Jahmyr Gibbs     17       63      250           1412               362.9 22.784394                254.070816
     De'Von Achane     17       87      203            907               299.9 23.216975                243.156525
       Chase Brown     16       65      229            990               255.0 24.780287                240.900925
      James Conner     16       55      236           1094               253.8 29.659138                235.259689
      Alvin Kamara     14       89      228            950               265.3 29.437372                235.202789
       Josh Jacobs     17       43      301           1329               293.1 26.885695                235.000076
    Bijan Robinson     17       72      304           1456               341.7 22.918549                229.153122
Kenneth Walker III     11       53      153            573               181.2 24.197125                225.678040
    Kyren Williams     16       40      316           1299               272.1 24.347707                222.930099
        James Cook     16       38      207           1009               266.7 25.267625                221.701492
      Bucky Irving     17       52      207           1122               244.4 22.368241                220.723526
       Breece Hall     16       76      209            876               240.9 23.586585                217.876007
     Chuba Hubbard     15       54      250           1195               241.6 25.557837                216.511978
   Jonathan Taylor     14       31      303           1431               244.7 25.949350                210.813110
         Joe Mixon     14       52      245           1016               240.5 28.438056                207.140472
     Derrick Henry     17       22      325           1921               336.4 30.989733                190.972794
    Saquon Barkley     16       43      345           2005               355.3 27.890486                190.476898
      J.K. Dobbins     13       38      195            905               191.8 26.039699                187.058167
     D'Andre Swift     17       52      253            959               214.5 25.963039                185.649277
       Aaron Jones     17       62      255           1138               241.6 30.080767                184.474411

Top 20 TE Projections for 2025
   player_name  games  targets  receptions  receiving_yards  fantasy_points_ppr       age  projected_fantasy_points
  Trey McBride     16      147         111             1146              243.80 25.108830                208.229553
  Brock Bowers     17      153         112             1194              262.70 22.050650                207.608200
 George Kittle     15       94          78             1106              236.60 31.227926                196.648727
   Jonnu Smith     17      111          88              884              222.30 29.360712                177.812256
   Sam LaPorta     16       83          60              726              174.60 23.967146                156.621536
  Travis Kelce     16      133          97              823              195.40 35.238877                138.655319
    Cade Otton     14       87          59              600              140.60 25.713895                133.709976
  Tucker Kraft     17       70          50              707              163.30 24.158795                133.135025
Pat Freiermuth     17       78          65              653              170.30 26.184805                127.742012
  Mark Andrews     17       69          55              673              188.80 29.319644                123.597000
  Hunter Henry     16       97          66              674              145.40 30.067077                123.546501
  Mike Gesicki     16       83          65              665              141.50 29.245722                118.720474
    Kyle Pitts     17       74          47              602              131.20 24.235455                118.720421
     Zach Ertz     17       91          66              654              177.40 34.140999                117.440819
   David Njoku     11       97          64              505              148.50 28.476386                115.825432
Dalton Kincaid     13       75          44              448              100.80 25.204654                106.470978
 Juwan Johnson     15       66          50              548              122.80 28.298426                102.048286
   Taysom Hill      8       31          23              187              102.34 34.357290                102.047668
Dallas Goedert     10       52          42              496              103.60 29.993155                100.313927
     Noah Gray     16       49          40              437              113.30 25.672827                 98.081116

Notes: Retuning massively shook up rankings! Model still seems to lean bearish on projections. These are the first results I've compared to a major model, in this case, ESPN's Mike Clay's 2025 Projection Guide (via https://g.espncdn.com/s/ffldraftkit/25/NFLDK2025_CS_ClayProjections2025.pdf). He projected 32 players to score over 252 fantasy points in 2025, while this model projects just 2 players to beat that mark. That said, these rankings are absolutely fathomable as far as the players included and their order. One glaring omission is Christian McCaffrey. I suspect the model is low on him due to having an injury-riddled 2024, playing in only four games. While some people do tend to avoid injured/injury-prone players when drafting fantasy teams, to exclude one of the all time great fantasy players at the back end of his prime seems like a major miscalculation.

# Model Tuning

### XGBoost Tuning experiment
Created a hyperparameter tuner that used the 2024 validation split for tuning and tested varying values for max_depth, learning_rate, and reg_lambda.

Best params for final model (by position):
WR: {'max_depth': 4, 'learning_rate': np.float64(0.06999999999999999), 'reg_lambda': np.float64(2.5)}
RB: {'max_depth': 2, 'learning_rate': np.float64(0.072), 'reg_lambda': np.float64(2.5)}
TE: {'max_depth': 2, 'learning_rate': np.float64(0.06), 'reg_lambda': np.float64(1.6)}