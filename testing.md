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