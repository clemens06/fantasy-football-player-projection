import pandas as pd

from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

from xgboost import XGBRegressor

import numpy as np

# ============================================================
# 1. LOAD DATA
# ============================================================

df_2018 = pd.read_csv("data/raw/stats_player_week_2018.csv",low_memory=False)
df_2019 = pd.read_csv("data/raw/stats_player_week_2019.csv",low_memory=False)
df_2020 = pd.read_csv("data/raw/stats_player_week_2020.csv",low_memory=False)
df_2021 = pd.read_csv("data/raw/stats_player_week_2021.csv",low_memory=False)
df_2022 = pd.read_csv("data/raw/stats_player_week_2022.csv",low_memory=False)
df_2023 = pd.read_csv("data/raw/stats_player_week_2023.csv",low_memory=False)
df_2024 = pd.read_csv("data/raw/stats_player_week_2024.csv",low_memory=False)
players_df = pd.read_csv("data/raw/players.csv",low_memory=False)

# Combine NFL data
nfl_df = pd.concat([df_2018, df_2019, df_2020, df_2021, df_2022, df_2023, df_2024],ignore_index=True)

# Only regular season
nfl_df = nfl_df[nfl_df["season_type"] == "REG"].copy()

# ============================================================
# 2. FILTER BY POSITION
# ============================================================

#create a separate WR dataframe
wr_df = nfl_df[nfl_df["position"] == "WR"].copy()

# Sum team pass attempts per week, from QB rows in the full weekly dataset
team_attempts = (nfl_df[nfl_df["position"] == "QB"]
    .groupby(["season", "week", "team"])["attempts"]
    .sum()
    .reset_index()
    .rename(columns={"attempts": "team_pass_attempts"})
)

# Merge onto the weekly WR data using season, week, and team
wr_df = wr_df.merge(team_attempts,on=["season", "week", "team"],how="left")

#create a separate RB dataframe
rb_df = nfl_df[nfl_df["position"] == "RB"].copy()

#add team pass attempts to RB dataframe as well
rb_df = rb_df.merge(team_attempts,on=["season", "week", "team"],how="left")

#create a separate TE dataframe
te_df = nfl_df[nfl_df["position"] == "TE"].copy()

#add team pass attempts to TE dataframe as well
te_df = te_df.merge(team_attempts,on=["season", "week", "team"],how="left")

# ============================================================
# 3. CREATE SEASON-LEVEL POSITIONAL DATA
# ============================================================

# IMPORTANT:
# Group by player_id, NOT player_name. player_id is the actual identity of the player.
# This prevents cases like Nathaniel "Tank" Dell appearing as N.Dell and T.Dell from becoming separate players.

wr_season = (wr_df.groupby(["season", "player_id"])
    .agg(
        games=("game_id", "nunique"),
        targets=("targets", "sum"),
        receptions=("receptions", "sum"),
        receiving_yards=("receiving_yards", "sum"),
        receiving_tds=("receiving_tds", "sum"),
        fantasy_points=("fantasy_points", "sum"),
        fantasy_points_ppr=("fantasy_points_ppr", "sum"),
        team_pass_attempts=("team_pass_attempts", "sum"),
        carries=("carries", "sum"),
        rushing_yards=("rushing_yards", "sum"),
        rushing_tds=("rushing_tds", "sum")
    )
    .reset_index()
)

rb_season = (rb_df.groupby(["season", "player_id"])
    .agg(
        games=("game_id", "nunique"),
        carries=("carries", "sum"),
        rushing_yards=("rushing_yards", "sum"),
        rushing_tds=("rushing_tds", "sum"),
        targets=("targets", "sum"),
        receptions=("receptions", "sum"),
        receiving_yards=("receiving_yards", "sum"),
        receiving_tds=("receiving_tds", "sum"),
        fantasy_points=("fantasy_points", "sum"),
        fantasy_points_ppr=("fantasy_points_ppr", "sum"),
        team_pass_attempts=("team_pass_attempts", "sum")
    )
    .reset_index()
)

te_season = (te_df.groupby(["season", "player_id"])
    .agg(
        games=("game_id", "nunique"),
        carries=("carries", "sum"),
        rushing_yards=("rushing_yards", "sum"),
        rushing_tds=("rushing_tds", "sum"),
        targets=("targets", "sum"),
        receptions=("receptions", "sum"),
        receiving_yards=("receiving_yards", "sum"),
        receiving_tds=("receiving_tds", "sum"),
        fantasy_points=("fantasy_points", "sum"),
        fantasy_points_ppr=("fantasy_points_ppr", "sum"),
        team_pass_attempts=("team_pass_attempts", "sum")
    )
    .reset_index()
)

# ============================================================
# 4. ADD OFFICIAL PLAYER INFORMATION + AGE
# ============================================================

player_data = players_df[["gsis_id","display_name","birth_date"]].copy()
player_data["birth_date"] = pd.to_datetime(player_data["birth_date"],errors="coerce")

# Merge player information
wr_season = wr_season.merge(player_data,left_on="player_id",right_on="gsis_id",how="left")
rb_season = rb_season.merge(player_data,left_on="player_id",right_on="gsis_id",how="left")
te_season = te_season.merge(player_data,left_on="player_id",right_on="gsis_id",how="left")

# Remove duplicate ID column
wr_season = wr_season.drop(columns=["gsis_id"])
rb_season = rb_season.drop(columns=["gsis_id"])
te_season = te_season.drop(columns=["gsis_id"])

# Rename official name to player_name
wr_season = wr_season.rename(columns={"display_name": "player_name"})
rb_season = rb_season.rename(columns={"display_name": "player_name"})
te_season = te_season.rename(columns={"display_name": "player_name"})

# Calculate age at end of season
for df in [wr_season, rb_season, te_season]:
    df["season_end"] = pd.to_datetime(df["season"].astype(str) + "-12-31")
    df["age"] = (df["season_end"] - df["birth_date"]).dt.days / 365.25

# Age curve: peak around 27, then decline
    df["age_sq"] = df["age"] ** 2
    df["age_curve"] = np.exp(-((df["age"] - 27.5) ** 2) / (2 * 4.5 ** 2))
    df["prime_age_bonus"] = np.where(df["age"].between(24, 29), 1, 0)
    df["post_30_decline"] = np.maximum(df["age"] - 30, 0)

# ============================================================
# 5. CREATE FEATURES
# ============================================================

#wr_season features
wr_season["targets_per_game"] = (wr_season["targets"]/ wr_season["games"])
wr_season["receptions_per_game"] = (wr_season["receptions"]/ wr_season["games"])
wr_season["receiving_yards_per_game"] = (wr_season["receiving_yards"]/ wr_season["games"])
wr_season["catch_rate"] = (wr_season["receptions"]/ wr_season["targets"])
wr_season["yards_per_target"] = (wr_season["receiving_yards"]/ wr_season["targets"])
wr_season["yards_per_reception"] = (wr_season["receiving_yards"]/ wr_season["receptions"])
wr_season["fantasy_points_per_game"] = (wr_season["fantasy_points_ppr"]/ wr_season["games"])
wr_season["target_share"] = (wr_season["targets"] / wr_season["team_pass_attempts"])
wr_season["target_share"] = wr_season["target_share"].replace([float("inf"), -float("inf")], 0).fillna(0)
wr_season["rushing_yards_per_game"] = (wr_season["rushing_yards"]/ wr_season["games"])
wr_season["rushing_tds_per_game"] = (wr_season["rushing_tds"]/ wr_season["games"])
wr_season["carries_per_game"] = (wr_season["carries"]/ wr_season["games"])

#rb_season features
rb_season["carries_per_game"] = (rb_season["carries"]/ rb_season["games"])
rb_season["rushing_yards_per_game"] = (rb_season["rushing_yards"]/ rb_season["games"])
rb_season["rushing_tds_per_game"] = (rb_season["rushing_tds"]/ rb_season["games"])
rb_season["targets_per_game"] = (rb_season["targets"]/ rb_season["games"])
rb_season["receptions_per_game"] = (rb_season["receptions"]/ rb_season["games"])
rb_season["receiving_yards_per_game"] = (rb_season["receiving_yards"]/ rb_season["games"])
rb_season["catch_rate"] = (rb_season["receptions"]/ rb_season["targets"])
rb_season["yards_per_target"] = (rb_season["receiving_yards"]/ rb_season["targets"])
rb_season["yards_per_reception"] = (rb_season["receiving_yards"]/ rb_season["receptions"])
rb_season["fantasy_points_per_game"] = (rb_season["fantasy_points_ppr"]/ rb_season["games"])
rb_season["target_share"] = (rb_season["targets"] / rb_season["team_pass_attempts"])
rb_season["target_share"] = rb_season["target_share"].replace([float("inf"), -float("inf")], 0).fillna(0)

#te_season features
te_season["targets_per_game"] = (te_season["targets"]/ te_season["games"])
te_season["receptions_per_game"] = (te_season["receptions"]/ te_season["games"])
te_season["receiving_yards_per_game"] = (te_season["receiving_yards"]/ te_season["games"])
te_season["catch_rate"] = (te_season["receptions"]/ te_season["targets"])
te_season["yards_per_target"] = (te_season["receiving_yards"]/ te_season["targets"])
te_season["yards_per_reception"] = (te_season["receiving_yards"]/ te_season["receptions"])
te_season["fantasy_points_per_game"] = (te_season["fantasy_points_ppr"]/ te_season["games"])
te_season["target_share"] = (te_season["targets"] / te_season["team_pass_attempts"])
te_season["target_share"] = te_season["target_share"].replace([float("inf"), -float("inf")], 0).fillna(0)
te_season["rushing_yards_per_game"] = (te_season["rushing_yards"]/ te_season["games"])
te_season["rushing_tds_per_game"] = (te_season["rushing_tds"]/ te_season["games"])
te_season["carries_per_game"] = (te_season["carries"]/ te_season["games"])

# Replace undefined ratios with 0
ratio_columns = [
    "targets_per_game",
    "receptions_per_game",
    "receiving_yards_per_game",
    "catch_rate",
    "yards_per_target",
    "yards_per_reception",
    "fantasy_points_per_game",
    "rushing_yards_per_game",
    "rushing_tds_per_game",
    "carries_per_game"
]

wr_season[ratio_columns] = (wr_season[ratio_columns].replace([float("inf"), -float("inf")],0).fillna(0))
rb_season[ratio_columns] = (rb_season[ratio_columns].replace([float("inf"), -float("inf")],0).fillna(0))
te_season[ratio_columns] = (te_season[ratio_columns].replace([float("inf"), -float("inf")],0).fillna(0))

# ============================================================
# 6. CREATE NEXT-SEASON TARGET
# ============================================================

wr_season["next_season"] = (wr_season["season"] + 1)
rb_season["next_season"] = (rb_season["season"] + 1)
te_season["next_season"] = (te_season["season"] + 1)

future_wr = wr_season[["season","player_id","fantasy_points_ppr"]].copy()
future_wr = future_wr.rename(columns={"season": "next_season","fantasy_points_ppr":"next_fantasy_points"})
wr_model_df = wr_season.merge(future_wr,on=["next_season","player_id"],how="inner")

future_rb = rb_season[["season","player_id","fantasy_points_ppr"]].copy()
future_rb = future_rb.rename(columns={"season": "next_season","fantasy_points_ppr":"next_fantasy_points"})
rb_model_df = rb_season.merge(future_rb,on=["next_season","player_id"],how="inner")

future_te = te_season[["season","player_id","fantasy_points_ppr"]].copy()
future_te = future_te.rename(columns={"season": "next_season","fantasy_points_ppr":"next_fantasy_points"})
te_model_df = te_season.merge(future_te,on=["next_season","player_id"],how="inner")

# Previous-season fantasy points
wr_model_df["previous_fantasy_points"] = (wr_model_df["fantasy_points_ppr"])
rb_model_df["previous_fantasy_points"] = (rb_model_df["fantasy_points_ppr"])
te_model_df["previous_fantasy_points"] = (te_model_df["fantasy_points_ppr"])

for df in [wr_model_df, rb_model_df, te_model_df]:
    df.sort_values(["player_id", "season"], inplace=True)
    df["prev_2yr_avg"] = (df.groupby("player_id")["fantasy_points_ppr"].transform(lambda s: s.shift(1).rolling(2, min_periods=1).mean()))
    df["fantasy_points_change"] = (df["fantasy_points_ppr"] - df["prev_2yr_avg"])
    df["breakout_flag"] = (df["fantasy_points_change"] > 5).astype(int)

# ============================================================
# 7. DEFINE FEATURES
# ============================================================

wr_features = [
    "targets",
    "receptions",
    "receiving_yards",
    "receiving_tds",
    "games",
    "targets_per_game",
    "receptions_per_game",
    "receiving_yards_per_game",
    "previous_fantasy_points",
    "catch_rate",
    "yards_per_target",
    "yards_per_reception",
    "fantasy_points_per_game",
    "age",
    "age_sq",
    "age_curve",
    "prime_age_bonus",
    "post_30_decline",
    "target_share",
    "rushing_yards",
    "rushing_tds",
    "carries",
    "rushing_yards_per_game",
    "rushing_tds_per_game",
    "carries_per_game",
    "prev_2yr_avg",
    "fantasy_points_change",
    "breakout_flag"
]

rb_features = [
    "targets",
    "receptions",
    "receiving_yards",
    "receiving_tds",
    "games",
    "targets_per_game",
    "receptions_per_game",
    "receiving_yards_per_game",
    "previous_fantasy_points",
    "catch_rate",
    "yards_per_target",
    "yards_per_reception",
    "fantasy_points_per_game",
    "age",
    "age_sq",
    "age_curve",
    "prime_age_bonus",
    "post_30_decline",
    "target_share",
    "rushing_yards",
    "rushing_tds",
    "carries",
    "rushing_yards_per_game",
    "rushing_tds_per_game",
    "carries_per_game",
    "prev_2yr_avg",
    "fantasy_points_change",
    "breakout_flag"
]

te_features = [
    "targets",
    "receptions",
    "receiving_yards",
    "receiving_tds",
    "games",
    "targets_per_game",
    "receptions_per_game",
    "receiving_yards_per_game",
    "previous_fantasy_points",
    "catch_rate",
    "yards_per_target",
    "yards_per_reception",
    "fantasy_points_per_game",
    "age",
    "age_sq",
    "age_curve",
    "prime_age_bonus",
    "post_30_decline",
    "target_share",
    "rushing_yards",
    "rushing_tds",
    "carries",
    "rushing_yards_per_game",
    "rushing_tds_per_game",
    "carries_per_game",
    "prev_2yr_avg",
    "fantasy_points_change",
    "breakout_flag"
]

# Missing values cleaning
for df in [wr_model_df, rb_model_df, te_model_df]:
    # Fill age with player's own average, then position median
    df["age"] = df.groupby("player_id")["age"].transform(
        lambda x: x.fillna(x.mean())
    )
    position_median_age = df["age"].median()
    df["age"] = df["age"].fillna(position_median_age)
    
    # Recalculate age-derived features
    df["age_sq"] = df["age"] ** 2
    df["age_curve"] = np.exp(-((df["age"] - 27.5) ** 2) / (2 * 4.5 ** 2))
    df["prime_age_bonus"] = np.where(df["age"].between(24, 29), 1, 0)
    df["post_30_decline"] = np.maximum(df["age"] - 30, 0)
    
    # Fill trend/breakout features with 0 (no prior data)
    df["prev_2yr_avg"] = df["prev_2yr_avg"].fillna(0)
    df["fantasy_points_change"] = df["fantasy_points_change"].fillna(0)
    df["breakout_flag"] = df["breakout_flag"].fillna(0)
    
    # Fill ratio features with 0
    ratio_columns = [
        "targets_per_game",
        "receptions_per_game",
        "receiving_yards_per_game",
        "catch_rate",
        "yards_per_target",
        "yards_per_reception",
        "fantasy_points_per_game",
        "rushing_yards_per_game",
        "rushing_tds_per_game",
        "carries_per_game",
        "target_share"
    ]
    
    for col in ratio_columns:
        if col in df.columns:
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)
            df[col] = df[col].fillna(0)


# ============================================================
# 8. CROSS-SEASON MODEL VALIDATION
# ============================================================

print()
print("=" * 60)
print("CROSS-SEASON MODEL VALIDATION")
print("=" * 60)

pos_feature_map = {"WR": wr_features,"RB": rb_features,"TE": te_features}

position_dfs = {"WR": wr_model_df,"RB": rb_model_df,"TE": te_model_df}

validation_results = []

for prediction_season in [2020, 2021, 2022, 2023, 2024]:
    for pos_name, pos_df in position_dfs.items():
        train_df = pos_df[pos_df["next_season"] < prediction_season].copy()
        test_df = pos_df[pos_df["next_season"] == prediction_season].copy()

        X_train = train_df[pos_feature_map[pos_name]]
        y_train = train_df["next_fantasy_points"]

        X_test = test_df[pos_feature_map[pos_name]]
        y_test = test_df["next_fantasy_points"]

        print()
        print(f"Predicting: {prediction_season} | Position: {pos_name}")
        print("Training:", X_train.shape)
        print("Testing:", X_test.shape)

        # Baseline
        baseline_predictions = (test_df["previous_fantasy_points"])
        baseline_mae = mean_absolute_error(y_test,baseline_predictions)
        print("Baseline MAE:",round(baseline_mae, 2))

        # Linear Regression
        linear_model = LinearRegression()
        linear_model.fit(X_train, y_train)
        linear_predictions = (linear_model.predict(X_test))
        linear_mae = mean_absolute_error(y_test,linear_predictions)
        print("Linear Regression MAE:", round(linear_mae, 2))

        # Ridge Regression
        ridge_model = Ridge(alpha=1.0)
        ridge_model.fit(X_train,y_train)
        ridge_predictions = (ridge_model.predict(X_test))
        ridge_mae = mean_absolute_error(y_test,ridge_predictions)
        print("Ridge Regression MAE:",round(ridge_mae, 2))

        # Random Forest
        rf_model = RandomForestRegressor(n_estimators=300,max_depth=8,random_state=42)
        rf_model.fit(X_train,y_train)
        rf_predictions = (rf_model.predict(X_test))
        rf_mae = mean_absolute_error(y_test,rf_predictions)
        print("Random Forest MAE:",round(rf_mae, 2))

        # XGBoost
        from xgboost import XGBRegressor
        xgb_model = XGBRegressor(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.05,
        reg_lambda=5.0,
        subsample=0.8,
        random_state=42
        )

        xgb_model.fit(X_train, y_train)
        xgb_predictions = xgb_model.predict(X_test)
        xgb_mae = mean_absolute_error(y_test, xgb_predictions)
        print("XGBoost MAE:", round(xgb_mae, 2))

        # Simple Ensemble (Linear + XGBoost average)
        ensemble_predictions = (linear_predictions + xgb_predictions) / 2
        ensemble_mae = mean_absolute_error(y_test,ensemble_predictions)
        print("Ensemble MAE:",round(ensemble_mae, 2))

        model_maes = {
            "Linear Regression": linear_mae,
            "Ridge Regression": ridge_mae,
            "Baseline": baseline_mae,
            "Random Forest": rf_mae,
            "XGBoost": xgb_mae,
            "Ensemble": ensemble_mae
        }

        best_model_name, best_model_mae = min(model_maes.items(),key=lambda x: x[1])

        print("Best model this season:", best_model_name, "(MAE:", round(best_model_mae, 2), ")")

        validation_results.append({
            "season": prediction_season,
            "position": pos_name,
            "linear_mae": linear_mae,
            "ridge_mae": ridge_mae,
            "baseline_mae": baseline_mae,
            "random_forest_mae": rf_mae,
            "xgboost_mae": xgb_mae,
            "ensemble_mae": ensemble_mae,
            "best_model": best_model_name,
            "best_mae": best_model_mae
            })

# ============================================================
# 9. XGBoost  FEATURE IMPORTANCE
# ============================================================

print()
print("=" * 60)
print("XGBoost FEATURE IMPORTANCE")
print("=" * 60)

position_models = {}

for pos_name, pos_df in position_dfs.items():
    model = XGBRegressor(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.05,
        reg_lambda=5.0,
        subsample=0.8,
        random_state=42
    )
    model.fit(pos_df[pos_feature_map[pos_name]],pos_df["next_fantasy_points"])
    position_models[pos_name] = model

for pos_name, model in position_models.items():
    importance_df = pd.DataFrame({"feature": pos_feature_map[pos_name],"importance": model.feature_importances_}).sort_values("importance", ascending=False)

    print()
    print(f"{pos_name} feature importance:")
    print(importance_df.head(20).to_string(index=False))

# ============================================================
# 10. MODEL SUMMARY
# ============================================================

print()
print("=" * 60)
print("MODEL SUMMARY")
print("=" * 60)

print(f"Training rows: {len(wr_model_df)}")
print(f"Training rows: {len(rb_model_df)}")
print(f"Training rows: {len(te_model_df)}")
print(f"Features: {len(pos_feature_map[pos_name])}")

summary_df = pd.DataFrame(validation_results)

print()
print(summary_df.head())

# average MAE by position
pos_avg_mae = (summary_df.groupby("position")["best_mae"].mean().sort_values())

print()
print("Average best MAE by position:")
print(pos_avg_mae)

model_cols = [
    "linear_mae",
    "ridge_mae",
    "baseline_mae",
    "random_forest_mae",
    "xgboost_mae",
    "ensemble_mae"
]

# average MAE per model across seasons
avg_mae_by_model = summary_df[model_cols].mean()
overall_best_model = avg_mae_by_model.idxmin()
overall_best_mae = avg_mae_by_model.min()

print()
print("=" * 60)
print("OVERALL BEST MODEL")
print("=" * 60)
print("Best model by average MAE:", overall_best_model)
print("Average MAE:", round(overall_best_mae, 2))
print(avg_mae_by_model.round(3))

# ============================================================
# 11. GENERATE 2025 PROJECTIONS
# ============================================================

print()
print("=" * 60)
print("2025 WR PROJECTIONS")
print("=" * 60)

final_models = {}

for pos_name, pos_df in position_dfs.items():
    final_model = XGBRegressor(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.05,
        reg_lambda=5.0,
        subsample=0.8,
        random_state=42
    )

    final_model.fit(pos_df[pos_feature_map[pos_name]],pos_df["next_fantasy_points"])
    final_models[pos_name] = final_model

# WR projection generation
wr_projection_df = wr_season[wr_season["season"] == 2024].copy()
wr_projection_df["previous_fantasy_points"] = wr_projection_df["fantasy_points_ppr"]
wr_projection_df["age"] = wr_projection_df["age"].fillna(wr_projection_df["age"].median())

# Add trend features
wr_projection_df = wr_projection_df.sort_values(["player_id", "season"])
wr_projection_df["prev_2yr_avg"] = wr_projection_df.groupby("player_id")["fantasy_points_ppr"].transform(
    lambda s: s.shift(1).rolling(2, min_periods=1).mean()
)
wr_projection_df["fantasy_points_change"] = wr_projection_df["fantasy_points_ppr"] - wr_projection_df["prev_2yr_avg"]
wr_projection_df["breakout_flag"] = (wr_projection_df["fantasy_points_change"] > 5).astype(int)
wr_projection_df["prev_2yr_avg"] = wr_projection_df["prev_2yr_avg"].fillna(0)
wr_projection_df["fantasy_points_change"] = wr_projection_df["fantasy_points_change"].fillna(0)
wr_projection_df["breakout_flag"] = wr_projection_df["breakout_flag"].fillna(0)

wr_projection_df["projected_fantasy_points"] = final_models["WR"].predict(
    wr_projection_df[pos_feature_map["WR"]]
)
wr_projection_df = wr_projection_df.sort_values("projected_fantasy_points", ascending=False)

print()
print("Top 10 WR Projections for 2025")
print(
    wr_projection_df[
        [
            "player_name",
            "games",
            "targets",
            "receptions",
            "receiving_yards",
            "fantasy_points_ppr",
            "age",
            "projected_fantasy_points"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

# RB projection generation
rb_projection_df = rb_season[rb_season["season"] == 2024].copy()
rb_projection_df["previous_fantasy_points"] = rb_projection_df["fantasy_points_ppr"]
rb_projection_df["age"] = rb_projection_df["age"].fillna(rb_projection_df["age"].median())

# Add trend features
rb_projection_df = rb_projection_df.sort_values(["player_id", "season"])
rb_projection_df["prev_2yr_avg"] = rb_projection_df.groupby("player_id")["fantasy_points_ppr"].transform(
    lambda s: s.shift(1).rolling(2, min_periods=1).mean()
)
rb_projection_df["fantasy_points_change"] = rb_projection_df["fantasy_points_ppr"] - rb_projection_df["prev_2yr_avg"]
rb_projection_df["breakout_flag"] = (rb_projection_df["fantasy_points_change"] > 5).astype(int)
rb_projection_df["prev_2yr_avg"] = rb_projection_df["prev_2yr_avg"].fillna(0)
rb_projection_df["fantasy_points_change"] = rb_projection_df["fantasy_points_change"].fillna(0)
rb_projection_df["breakout_flag"] = rb_projection_df["breakout_flag"].fillna(0)

rb_projection_df["projected_fantasy_points"] = final_models["RB"].predict(
    rb_projection_df[pos_feature_map["RB"]]
)
rb_projection_df = rb_projection_df.sort_values("projected_fantasy_points", ascending=False)

print()
print("Top 10 RB Projections for 2025")
print(
    rb_projection_df[
        [
            "player_name",
            "games",
            "targets",
            "receptions",
            "receiving_yards",
            "fantasy_points_ppr",
            "age",
            "projected_fantasy_points"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

# TE projection generation
te_projection_df = te_season[te_season["season"] == 2024].copy()
te_projection_df["previous_fantasy_points"] = te_projection_df["fantasy_points_ppr"]
te_projection_df["age"] = te_projection_df["age"].fillna(te_projection_df["age"].median())

# Add trend features
te_projection_df = te_projection_df.sort_values(["player_id", "season"])
te_projection_df["prev_2yr_avg"] = te_projection_df.groupby("player_id")["fantasy_points_ppr"].transform(
    lambda s: s.shift(1).rolling(2, min_periods=1).mean()
)
te_projection_df["fantasy_points_change"] = te_projection_df["fantasy_points_ppr"] - te_projection_df["prev_2yr_avg"]
te_projection_df["breakout_flag"] = (te_projection_df["fantasy_points_change"] > 5).astype(int)
te_projection_df["prev_2yr_avg"] = te_projection_df["prev_2yr_avg"].fillna(0)
te_projection_df["fantasy_points_change"] = te_projection_df["fantasy_points_change"].fillna(0)
te_projection_df["breakout_flag"] = te_projection_df["breakout_flag"].fillna(0)

te_projection_df["projected_fantasy_points"] = final_models["TE"].predict(
    te_projection_df[pos_feature_map["TE"]]
)
te_projection_df = te_projection_df.sort_values("projected_fantasy_points", ascending=False)

print()
print("Top 10 TE Projections for 2025")
print(
    te_projection_df[
        [
            "player_name",
            "games",
            "targets",
            "receptions",
            "receiving_yards",
            "fantasy_points_ppr",
            "age",
            "projected_fantasy_points"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

# ============================================================
# 12. 2024 MODEL ERROR ANALYSIS
# ============================================================

# Recreate 2024 test set explicitly
wr_train_df = wr_model_df[wr_model_df["next_season"] < 2024]
wr_test_df = wr_model_df[wr_model_df["next_season"] == 2024]
wr_X_train = wr_train_df[pos_feature_map["WR"]]
wr_y_train = wr_train_df["next_fantasy_points"]
wr_X_test = wr_test_df[pos_feature_map["WR"]]
wr_y_test = wr_test_df["next_fantasy_points"]

rb_train_df = rb_model_df[rb_model_df["next_season"] < 2024]
rb_test_df = rb_model_df[rb_model_df["next_season"] == 2024]
rb_X_train = rb_train_df[pos_feature_map["RB"]]
rb_y_train = rb_train_df["next_fantasy_points"]
rb_X_test = rb_test_df[pos_feature_map["RB"]]
rb_y_test = rb_test_df["next_fantasy_points"]

te_train_df = te_model_df[te_model_df["next_season"] < 2024]
te_test_df = te_model_df[te_model_df["next_season"] == 2024]
te_X_train = te_train_df[pos_feature_map["TE"]]
te_y_train = te_train_df["next_fantasy_points"]
te_X_test = te_test_df[pos_feature_map["TE"]]
te_y_test = te_test_df["next_fantasy_points"]

# Train 2024 evaluation model

wr_rf_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=8,
    random_state=42
)

rb_rf_model = RandomForestRegressor(
    n_estimators=300, 
    max_depth=8,
    random_state=42
)

te_rf_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=8,
    random_state=42
)

wr_rf_model.fit(wr_X_train,wr_y_train)
rb_rf_model.fit(rb_X_train,rb_y_train)
te_rf_model.fit(te_X_train,te_y_train)

wr_predictions = wr_rf_model.predict(wr_X_test)
rb_predictions = rb_rf_model.predict(rb_X_test)
te_predictions = te_rf_model.predict(te_X_test)

wr_comparison = wr_test_df[["player_id","player_name","next_fantasy_points"]].copy()
rb_comparison = rb_test_df[["player_id","player_name","next_fantasy_points"]].copy()
te_comparison = te_test_df[["player_id","player_name","next_fantasy_points"]].copy()

wr_comparison["predicted"] = wr_predictions
rb_comparison["predicted"] = rb_predictions
te_comparison["predicted"] = te_predictions

wr_comparison["error"] = (wr_comparison["predicted"] - wr_comparison["next_fantasy_points"])
rb_comparison["error"] = (rb_comparison["predicted"] - rb_comparison["next_fantasy_points"])
te_comparison["error"] = (te_comparison["predicted"] - te_comparison["next_fantasy_points"])

wr_comparison["absolute_error"] = (wr_comparison["error"].abs())
rb_comparison["absolute_error"] = (rb_comparison["error"].abs())
te_comparison["absolute_error"] = (te_comparison["error"].abs())

# ============================================================
# 13. BIGGEST OVERPREDICTIONS
# ============================================================

print()
print("=" * 60)
print("BIGGEST OVERPREDICTIONS")
print("=" * 60)

print()
print("WR")
print(wr_comparison.sort_values("error",ascending=False)[
        [
            "player_name",
            "next_fantasy_points",
            "predicted",
            "error"
        ]
    ]
    .head(20)
)

print()
print("RB")
print(rb_comparison.sort_values("error",ascending=False)[
        [
            "player_name",
            "next_fantasy_points",
            "predicted",
            "error"
        ]
    ] 
    .head(20)
)

print()
print("TE")
print(te_comparison.sort_values("error",ascending=False)[
        [
            "player_name",
            "next_fantasy_points",
            "predicted",
            "error"
        ]
    ]
    .head(20)
)

# ============================================================
# 14. BIGGEST UNDERPREDICTIONS
# ============================================================

print()
print("=" * 60)
print("BIGGEST UNDERPREDICTIONS")
print("=" * 60)

print()
print("WR")
print(wr_comparison.sort_values("error")[
        [
            "player_name",
            "next_fantasy_points",
            "predicted",
            "error"
        ]
    ]
    .head(20)
)

print()
print("RB")
print(rb_comparison.sort_values("error")[
        [
            "player_name",
            "next_fantasy_points",
            "predicted",
            "error"
        ]
    ]
    .head(20)
)

print()
print("TE")
print(te_comparison.sort_values("error")[
        [
            "player_name",
            "next_fantasy_points",
            "predicted",
            "error"
        ]
    ]
    .head(20)
)

# ============================================================
# 15. LARGEST ABSOLUTE ERRORS
# ============================================================

print()
print("=" * 60)
print("LARGEST ABSOLUTE ERRORS")
print("=" * 60)

print()
print("WR")
print(wr_comparison.sort_values("absolute_error",ascending=False)[
        [
            "player_name",
            "next_fantasy_points",
            "predicted",
            "error"
        ]
    ]
    .head(20)
)

print()
print("RB")
print(rb_comparison.sort_values("absolute_error",ascending=False)[
        [
            "player_name",
            "next_fantasy_points",
            "predicted",
            "error"
        ]
    ]
    .head(20)
)

print()
print("TE")
print(te_comparison.sort_values("absolute_error",ascending=False)[
        [
            "player_name",
            "next_fantasy_points",
            "predicted",
            "error"
        ]
    ]
    .head(20)
)