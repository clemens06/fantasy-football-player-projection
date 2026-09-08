import pandas as pd

from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBRegressor

import numpy as np

from sklearn.linear_model import RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

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

# Sum team pass attempts per week, from QB rows in the full weekly dataset
team_attempts = (nfl_df[nfl_df["position"] == "QB"]
    .groupby(["season", "week", "team"])["attempts"]
    .sum()
    .reset_index()
    .rename(columns={"attempts": "team_pass_attempts"})
)

#create a separate WR dataframe
wr_df = nfl_df[nfl_df["position"] == "WR"].copy()

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

#create a separate QB dataframe
qb_df = nfl_df[nfl_df["position"] == "QB"].copy()
# ============================================================
# 3. CREATE SEASON-LEVEL POSITIONAL DATA
# ============================================================

# IMPORTANT:
# Group by player_id, NOT player_name. player_id is the actual identity of the player.
# This prevents cases like Nathaniel "Tank" Dell appearing as N.Dell and T.Dell
# from becoming separate players.

def build_season_table(position_df, agg_spec):
    return (
        position_df
        .groupby(["season", "player_id"])
        .agg(**agg_spec)
        .reset_index()
    )

agg_specs = {
    "WR": dict(
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
        rushing_tds=("rushing_tds", "sum"),
    ),
    "RB": dict(
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
        team_pass_attempts=("team_pass_attempts", "sum"),
    ),
    "TE": dict(
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
        team_pass_attempts=("team_pass_attempts", "sum"),
    ),
    "QB": dict(
        games=("game_id", "nunique"),
        passing_attempts=("attempts", "sum"),
        passing_completions=("completions", "sum"),
        passing_yards=("passing_yards", "sum"),
        passing_tds=("passing_tds", "sum"),
        passing_interceptions=("passing_interceptions", "sum"),
        fantasy_points=("fantasy_points", "sum"),
        fantasy_points_ppr=("fantasy_points_ppr", "sum"),
        rushing_yards=("rushing_yards", "sum"),
        rushing_tds=("rushing_tds", "sum"),
        carries=("carries", "sum"),
    ),
}

raw_position_dfs = {"WR": wr_df, "RB": rb_df, "TE": te_df, "QB": qb_df}

season_tables = {
    pos_name: build_season_table(raw_df, agg_specs[pos_name])
    for pos_name, raw_df in raw_position_dfs.items()
}

wr_season = season_tables["WR"]
rb_season = season_tables["RB"]
te_season = season_tables["TE"]
qb_season = season_tables["QB"]

# ============================================================
# 4. ADD OFFICIAL PLAYER INFORMATION + AGE
# ============================================================

player_data = players_df[["gsis_id","display_name","birth_date"]].copy()
player_data["birth_date"] = pd.to_datetime(player_data["birth_date"],errors="coerce")

# Merge player information
wr_season = wr_season.merge(player_data,left_on="player_id",right_on="gsis_id",how="left")
rb_season = rb_season.merge(player_data,left_on="player_id",right_on="gsis_id",how="left")
te_season = te_season.merge(player_data,left_on="player_id",right_on="gsis_id",how="left")
qb_season = qb_season.merge(player_data,left_on="player_id",right_on="gsis_id",how="left")

# Remove duplicate ID column
wr_season = wr_season.drop(columns=["gsis_id"])
rb_season = rb_season.drop(columns=["gsis_id"])
te_season = te_season.drop(columns=["gsis_id"])
qb_season = qb_season.drop(columns=["gsis_id"])

# Rename official name to player_name
wr_season = wr_season.rename(columns={"display_name": "player_name"})
rb_season = rb_season.rename(columns={"display_name": "player_name"})
te_season = te_season.rename(columns={"display_name": "player_name"})
qb_season = qb_season.rename(columns={"display_name": "player_name"})

# Calculate age at end of season
for df in [wr_season, rb_season, te_season, qb_season]:
    df["season_end"] = pd.to_datetime(df["season"].astype(str) + "-12-31")
    df["age"] = (df["season_end"] - df["birth_date"]).dt.days / 365.25

age_curve_params = {
    "RB": {"peak_age": 25.5, "width": 3.0},
    "WR": {"peak_age": 27.0, "width": 4.0},
    "TE": {"peak_age": 28.0, "width": 4.5},
    "QB": {"peak_age": 29.5, "width": 5.5},
}

def add_age_features(df, position):
    df = df.copy()
    params = age_curve_params[position]
    peak_age = params["peak_age"]
    width = params["width"]

    df["season_end"] = pd.to_datetime(df["season"].astype(str) + "-12-31")
    df["age"] = (df["season_end"] - df["birth_date"]).dt.days / 365.25

    df["age_sq"] = df["age"] ** 2
    df["age_curve"] = np.exp(-((df["age"] - peak_age) ** 2) / (2 * width ** 2))

    # Prime window: +/- 2 years around peak_age, rounded to whole years
    prime_low = round(peak_age - 2)
    prime_high = round(peak_age + 2)
    df["prime_age_bonus"] = np.where(df["age"].between(prime_low, prime_high), 1, 0)

    # Decline measured from each position's own peak, not a fixed age-30 cutoff
    df["post_peak_decline"] = np.maximum(df["age"] - peak_age, 0)

    return df

wr_season = add_age_features(wr_season, "WR")
rb_season = add_age_features(rb_season, "RB")
te_season = add_age_features(te_season, "TE")
qb_season = add_age_features(qb_season, "QB")

# ============================================================
# 5. CREATE FEATURES
# ============================================================

def add_rate_features(df):
    df = df.copy()

    # Any raw counting stat present gets a "_per_game" version.
    # Naming matches your original convention exactly (e.g. "targets" -> "targets_per_game").
    countable_columns = [
        "targets", "receptions", "receiving_yards", "rushing_yards",
        "rushing_tds", "carries", "passing_attempts", "passing_completions",
        "passing_yards", "passing_tds", "passing_interceptions",
    ]

    for col in countable_columns:
        if col in df.columns:
            df[f"{col}_per_game"] = df[col] / df["games"]

    df["fantasy_points_per_game"] = df["fantasy_points_ppr"] / df["games"]

    # Receiving efficiency stats only apply to positions with targets/receptions
    if {"receptions", "targets"}.issubset(df.columns):
        df["catch_rate"] = df["receptions"] / df["targets"]
    if {"receiving_yards", "targets"}.issubset(df.columns):
        df["yards_per_target"] = df["receiving_yards"] / df["targets"]
    if {"receiving_yards", "receptions"}.issubset(df.columns):
        df["yards_per_reception"] = df["receiving_yards"] / df["receptions"]
    if {"targets", "team_pass_attempts"}.issubset(df.columns):
        df["target_share"] = df["targets"] / df["team_pass_attempts"]

    # Clean up any divide-by-zero or missing-denominator results
    ratio_columns = [
        col for col in df.columns
        if col.endswith("_per_game")
        or col in ["catch_rate", "yards_per_target", "yards_per_reception", "target_share"]
    ]

    df[ratio_columns] = (
        df[ratio_columns]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0)
    )

    return df

wr_season = add_rate_features(wr_season)
rb_season = add_rate_features(rb_season)
te_season = add_rate_features(te_season)
qb_season = add_rate_features(qb_season)

# ============================================================
# 6. CREATE NEXT-SEASON TARGET
# ============================================================

wr_season["next_season"] = (wr_season["season"] + 1)
rb_season["next_season"] = (rb_season["season"] + 1)
te_season["next_season"] = (te_season["season"] + 1)
qb_season["next_season"] = (qb_season["season"] + 1)

future_wr = wr_season[["season","player_id","fantasy_points_ppr"]].copy()
future_wr = future_wr.rename(columns={"season": "next_season","fantasy_points_ppr":"next_fantasy_points"})
wr_model_df = wr_season.merge(future_wr,on=["next_season","player_id"],how="inner")

future_rb = rb_season[["season","player_id","fantasy_points_ppr"]].copy()
future_rb = future_rb.rename(columns={"season": "next_season","fantasy_points_ppr":"next_fantasy_points"})
rb_model_df = rb_season.merge(future_rb,on=["next_season","player_id"],how="inner")

future_te = te_season[["season","player_id","fantasy_points_ppr"]].copy()
future_te = future_te.rename(columns={"season": "next_season","fantasy_points_ppr":"next_fantasy_points"})
te_model_df = te_season.merge(future_te,on=["next_season","player_id"],how="inner")

future_qb = qb_season[["season","player_id","fantasy_points_ppr"]].copy()
future_qb = future_qb.rename(columns={"season": "next_season","fantasy_points_ppr":"next_fantasy_points"})
qb_model_df = qb_season.merge(future_qb,on=["next_season","player_id"],how="inner")

# Previous-season fantasy points
wr_model_df["previous_fantasy_points"] = (wr_model_df["fantasy_points_ppr"])
rb_model_df["previous_fantasy_points"] = (rb_model_df["fantasy_points_ppr"])
te_model_df["previous_fantasy_points"] = (te_model_df["fantasy_points_ppr"])
qb_model_df["previous_fantasy_points"] = (qb_model_df["fantasy_points_ppr"])

breakout_std_multiplier = 1.5
breakout_thresholds = {}  # stores each position's threshold so create_projection_df can reuse it

model_dfs = {"WR": wr_model_df, "RB": rb_model_df, "TE": te_model_df, "QB": qb_model_df}

for pos_name, df in model_dfs.items():
    df.sort_values(["player_id", "season"], inplace=True)

    df["prev_2yr_avg"] = (
        df.groupby("player_id")["fantasy_points_ppr"]
        .transform(lambda s: s.shift(1).rolling(2, min_periods=1).mean())
    )
    df["fantasy_points_change"] = df["fantasy_points_ppr"] - df["prev_2yr_avg"]

    position_change_std = df["fantasy_points_change"].dropna().std()
    threshold = breakout_std_multiplier * position_change_std
    breakout_thresholds[pos_name] = threshold

    df["breakout_flag"] = (df["fantasy_points_change"] > threshold).astype(int)

wr_model_df, rb_model_df, te_model_df, qb_model_df = (
    model_dfs["WR"], model_dfs["RB"], model_dfs["TE"], model_dfs["QB"]
)

print("Breakout thresholds by position:")
for pos_name, threshold in breakout_thresholds.items():
    print(f"  {pos_name}: {round(threshold, 2)} PPR points")

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
    "post_peak_decline",
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
    "post_peak_decline",
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
    "post_peak_decline",
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

qb_features = [
    "passing_yards",
    "passing_tds",
    "passing_interceptions",
    "passing_attempts",
    "passing_completions",
    "passing_yards_per_game",
    "passing_tds_per_game",
    "passing_interceptions_per_game",
    "passing_attempts_per_game",
    "passing_completions_per_game",
    "carries_per_game",
    "rushing_yards_per_game",
    "rushing_tds_per_game",
    "previous_fantasy_points",
    "fantasy_points_per_game",
    "carries",
    "rushing_yards",
    "rushing_tds",
    "age",
    "age_sq",
    "age_curve",
    "prime_age_bonus",
    "post_peak_decline",
    "prev_2yr_avg",
    "fantasy_points_change",
    "breakout_flag"
]
# Missing values cleaning
position_dfs = {"WR": wr_model_df, "RB": rb_model_df, "TE": te_model_df, "QB": qb_model_df}

for pos_name, df in position_dfs.items():
    params = age_curve_params[pos_name]
    peak_age = params["peak_age"]
    width = params["width"]
    prime_low = round(peak_age - 2)
    prime_high = round(peak_age + 2)

    # Fill age with player's own average, then position median
    df["age"] = df.groupby("player_id")["age"].transform(lambda x: x.fillna(x.mean()))
    df["age"] = df["age"].fillna(df["age"].median())

    # Recalculate age-derived features using this position's own curve
    df["age_sq"] = df["age"] ** 2
    df["age_curve"] = np.exp(-((df["age"] - peak_age) ** 2) / (2 * width ** 2))
    df["prime_age_bonus"] = np.where(df["age"].between(prime_low, prime_high), 1, 0)
    df["post_peak_decline"] = np.maximum(df["age"] - peak_age, 0)

    # Fill trend/breakout features with 0 (no prior data)
    df["prev_2yr_avg"] = df["prev_2yr_avg"].fillna(0)
    df["fantasy_points_change"] = df["fantasy_points_change"].fillna(0)
    df["breakout_flag"] = df["breakout_flag"].fillna(0)

    # Fill ratio features with 0
    ratio_columns = [
        "targets_per_game", "receptions_per_game", "receiving_yards_per_game",
        "catch_rate", "yards_per_target", "yards_per_reception",
        "fantasy_points_per_game", "rushing_yards_per_game", "rushing_tds_per_game",
        "carries_per_game", "target_share", "passing_attempts_per_game",
        "passing_completions_per_game", "passing_yards_per_game",
        "passing_tds_per_game", "passing_interceptions_per_game",
    ]

    for col in ratio_columns:
        if col in df.columns:
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)
            df[col] = df[col].fillna(0)
    
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
        "target_share",
        "passing_attempts_per_game",
        "passing_completions_per_game",
        "passing_yards_per_game",
        "passing_tds_per_game",
        "passing_interceptions_per_game",
        "sacks_per_game"
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

pos_feature_map = {"WR": wr_features,"RB": rb_features,"TE": te_features,"QB": qb_features}

position_dfs = {"WR": wr_model_df,"RB": rb_model_df,"TE": te_model_df,"QB": qb_model_df}

validation_results = []
tuning_results = []

for prediction_season in [2020, 2021, 2022, 2023, 2024]:
    for pos_name, pos_df in position_dfs.items():
        train_df = pos_df[pos_df["next_season"] < prediction_season].copy()
        test_df = pos_df[pos_df["next_season"] == prediction_season].copy()

        if train_df.empty or test_df.empty:
            continue

        X_train = train_df[pos_feature_map[pos_name]]
        y_train = train_df["next_fantasy_points"]
        X_test = test_df[pos_feature_map[pos_name]]
        y_test = test_df["next_fantasy_points"]

        # Must be inside both loops
        best_xgb_mae = float("inf")
        best_xgb_params = {
            "max_depth": 3,
            "learning_rate": 0.05,
            "reg_lambda": 5.0
        }

        training_seasons = sorted(train_df["next_season"].unique())

        if len(training_seasons) >= 2:
            inner_validation_season = training_seasons[-1]

            inner_train_df = train_df[
                train_df["next_season"] < inner_validation_season
            ]
            inner_validation_df = train_df[
                train_df["next_season"] == inner_validation_season
            ]

            X_inner_train = inner_train_df[pos_feature_map[pos_name]]
            y_inner_train = inner_train_df["next_fantasy_points"]
            X_inner_validation = inner_validation_df[pos_feature_map[pos_name]]
            y_inner_validation = inner_validation_df["next_fantasy_points"]

            for max_depth in [2, 3, 4, 5]:
                for learning_rate in [0.01, 0.05, 0.1]:
                    for reg_lambda in [0.5, 1.0, 5.0]:
                        candidate_model = XGBRegressor(
                            n_estimators=100,
                            max_depth=max_depth,
                            learning_rate=learning_rate,
                            reg_lambda=reg_lambda,
                            subsample=0.8,
                            random_state=42
                        )

                        candidate_model.fit(X_inner_train, y_inner_train)
                        inner_predictions = candidate_model.predict(
                            X_inner_validation
                        )
                        inner_mae = mean_absolute_error(
                            y_inner_validation,
                            inner_predictions
                        )

                        if inner_mae < best_xgb_mae:
                            best_xgb_mae = inner_mae
                            best_xgb_params = {
                                "max_depth": max_depth,
                                "learning_rate": learning_rate,
                                "reg_lambda": reg_lambda
                            }

        # This must be outside the if block, so 2020 is evaluated too
        xgb_model = XGBRegressor(
            n_estimators=100,
            **best_xgb_params,
            subsample=0.8,
            random_state=42
        )

        xgb_model.fit(X_train, y_train)
        xgb_predictions = xgb_model.predict(X_test)
        xgb_mae = mean_absolute_error(y_test, xgb_predictions)
        print("XGBoost parameters:", best_xgb_params)
        print("XGBoost MAE:", round(xgb_mae, 2))

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
        ridge_model = make_pipeline(
        StandardScaler(),
        RidgeCV(
        alphas=[0.01, 0.1, 1.0, 10.0, 100.0, 1000.0],
        scoring="neg_mean_absolute_error",
        cv=TimeSeriesSplit(n_splits=5)
    )
)
        ridge_model.fit(X_train, y_train)
        ridge_predictions = ridge_model.predict(X_test)
        selected_alpha = ridge_model.named_steps["ridgecv"].alpha_
        print("Ridge alpha:", selected_alpha)
        ridge_mae = mean_absolute_error(y_test,ridge_predictions)
        print("Ridge Regression MAE:",round(ridge_mae, 2))

        # Random Forest
        rf_model = RandomForestRegressor(n_estimators=300,max_depth=8,random_state=42)
        rf_model.fit(X_train,y_train)
        rf_predictions = (rf_model.predict(X_test))
        rf_mae = mean_absolute_error(y_test,rf_predictions)
        print("Random Forest MAE:",round(rf_mae, 2))

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

        print()

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

        tuning_results.append({
        "season": prediction_season,
        "position": pos_name,
        "xgb_max_depth": best_xgb_params["max_depth"],
        "xgb_learning_rate": best_xgb_params["learning_rate"],
        "xgb_reg_lambda": best_xgb_params["reg_lambda"],
        "tuning_mae": best_xgb_mae,
        "test_mae": xgb_mae
        })

#Tuning Xgboost
print()
print("=" * 60)
print("XGBoost HYPERPARAMETER TUNING")
print("=" * 60)

tuning_df = pd.DataFrame(tuning_results)
print(tuning_df.to_string(index=False))

# Select final parameters using average tuning MAE.
# Exclude 2020 rows because they have no inner validation season.
valid_tuning = tuning_df[
    np.isfinite(tuning_df["tuning_mae"])
].copy()

parameter_scores = (
    valid_tuning
    .groupby(
        [
            "position",
            "xgb_max_depth",
            "xgb_learning_rate",
            "xgb_reg_lambda"
        ],
        as_index=False
    )["tuning_mae"]
    .mean()
    .sort_values(["position", "tuning_mae"])
)

best_final_params = {}

for pos_name in position_dfs:
    position_scores = parameter_scores[
        parameter_scores["position"] == pos_name
    ]

    if position_scores.empty:
        best_final_params[pos_name] = {
            "max_depth": 3,
            "learning_rate": 0.05,
            "reg_lambda": 5.0
        }
    else:
        best_row = position_scores.iloc[0]

        best_final_params[pos_name] = {
            "max_depth": int(best_row["xgb_max_depth"]),
            "learning_rate": float(best_row["xgb_learning_rate"]),
            "reg_lambda": float(best_row["xgb_reg_lambda"])
        }

print()
print("Best params for final model:")
for pos_name, params in best_final_params.items():
    print(f"{pos_name}: {params}")

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
        max_depth=best_final_params[pos_name]['max_depth'],
        learning_rate=best_final_params[pos_name]['learning_rate'],
        reg_lambda=best_final_params[pos_name]['reg_lambda'],
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
print(f"Training rows: {len(qb_model_df)}")
print(f"Features: {len(pos_feature_map[pos_name])}")

summary_df = pd.DataFrame(validation_results)

print()
print(summary_df.head(15))

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
print("2025 PROJECTIONS")
print("=" * 60)

final_models = {}

for pos_name, pos_df in position_dfs.items():
    final_model = XGBRegressor(
        n_estimators=100,
        max_depth=best_final_params[pos_name]['max_depth'],
        learning_rate=best_final_params[pos_name]['learning_rate'],
        reg_lambda=best_final_params[pos_name]['reg_lambda'],
        subsample=0.8,
        random_state=42
    )

    final_model.fit(pos_df[pos_feature_map[pos_name]],pos_df["next_fantasy_points"])
    final_models[pos_name] = final_model

def create_projection_df(season_df, season, feature_columns, breakout_threshold):
    projection_df = season_df.copy()

    projection_df = projection_df.sort_values(["player_id", "season"]).copy()

    projection_df["prev_2yr_avg"] = (
        projection_df
        .groupby("player_id")["fantasy_points_ppr"]
        .transform(lambda values: values.shift(1).rolling(window=2, min_periods=1).mean())
    )

    projection_df["fantasy_points_change"] = (
        projection_df["fantasy_points_ppr"] - projection_df["prev_2yr_avg"]
    )

    projection_df["breakout_flag"] = (
        projection_df["fantasy_points_change"] > breakout_threshold
    ).astype(int)

    projection_df = projection_df[projection_df["season"] == season].copy()

    # ... rest of the function stays exactly the same ...

    projection_df["breakout_flag"] = (
        projection_df["fantasy_points_change"] > 25
    ).astype(int)

    # Select 2024 only after historical features are calculated
    projection_df = projection_df[
        projection_df["season"] == season
    ].copy()

    # Features based on the player's most recent season
    projection_df["previous_fantasy_points"] = (
        projection_df["fantasy_points_ppr"]
    )

    # Fill missing age using the position's median age
    projection_df["age"] = projection_df["age"].fillna(
        projection_df["age"].median()
    )

    # Recalculate age-derived features
    projection_df["age_sq"] = projection_df["age"] ** 2
    projection_df["age_curve"] = np.exp(
        -((projection_df["age"] - 27.5) ** 2)
        / (2 * 4.5 ** 2)
    )
    projection_df["prime_age_bonus"] = np.where(
        projection_df["age"].between(24, 29),
        1,
        0
    )
    projection_df["post_peak_decline"] = np.maximum(
        projection_df["age"] - 27.5,
        0
    )

    # Players with no previous seasons receive neutral trend values
    trend_columns = [
        "prev_2yr_avg",
        "fantasy_points_change",
        "breakout_flag"
    ]

    projection_df[trend_columns] = (
        projection_df[trend_columns]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0)
    )

    # Ensure every model feature is numeric and finite
    projection_df[feature_columns] = (
        projection_df[feature_columns]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0)
    )

    return projection_df


wr_projection_df = create_projection_df(wr_season, 2024, pos_feature_map["WR"], breakout_thresholds["WR"])
rb_projection_df = create_projection_df(rb_season, 2024, pos_feature_map["RB"], breakout_thresholds["RB"])
te_projection_df = create_projection_df(te_season, 2024, pos_feature_map["TE"], breakout_thresholds["TE"])
qb_projection_df = create_projection_df(qb_season, 2024, pos_feature_map["QB"], breakout_thresholds["QB"])

# Generate predictions
wr_projection_df["projected_fantasy_points"] = (
    final_models["WR"].predict(
        wr_projection_df[pos_feature_map["WR"]]
    )
)

rb_projection_df["projected_fantasy_points"] = (
    final_models["RB"].predict(
        rb_projection_df[pos_feature_map["RB"]]
    )
)

te_projection_df["projected_fantasy_points"] = (
    final_models["TE"].predict(
        te_projection_df[pos_feature_map["TE"]]
    )
)

qb_projection_df["projected_fantasy_points"] = (
    final_models["QB"].predict(
        qb_projection_df[pos_feature_map["QB"]]
    )
)

# Sort projections
wr_projection_df = wr_projection_df.sort_values(
    "projected_fantasy_points",
    ascending=False
)

rb_projection_df = rb_projection_df.sort_values(
    "projected_fantasy_points",
    ascending=False
)

te_projection_df = te_projection_df.sort_values(
    "projected_fantasy_points",
    ascending=False
)

qb_projection_df = qb_projection_df.sort_values(
    "projected_fantasy_points",
    ascending=False
)

print()
print("Top 20 WR Projections for 2025")
print(
    wr_projection_df[
        [
            "player_name",
            "age",
            "breakout_flag",
            "projected_fantasy_points"
        ]
    ]
    .head(20)
    .to_string(index=False)
)

print()
print("Top 20 RB Projections for 2025")
print(
    rb_projection_df[
        [
            "player_name",
            "age",
            "breakout_flag",
            "projected_fantasy_points"
        ]
    ]
    .head(20)
    .to_string(index=False)
)

print()
print("Top 20 TE Projections for 2025")
print(
    te_projection_df[
        [
            "player_name",
            "age",
            "breakout_flag",
            "projected_fantasy_points"
        ]
    ]
    .head(20)
    .to_string(index=False)
)

print()
print("Top 20 QB Projections for 2025")
print(
    qb_projection_df[
        [
            "player_name",
            "age",
            "breakout_flag",
            "projected_fantasy_points"
        ]
    ]
    .head(20)
    .to_string(index=False)
)
# ============================================================
# 12. 2024 MODEL ERROR ANALYSIS
# ============================================================

def evaluate_position_for_season(pos_name, model_df, feature_columns, xgb_params, prediction_season):
    train_df = model_df[model_df["next_season"] < prediction_season]
    test_df = model_df[model_df["next_season"] == prediction_season]

    X_train = train_df[feature_columns]
    y_train = train_df["next_fantasy_points"]
    X_test = test_df[feature_columns]
    y_test = test_df["next_fantasy_points"]

    eval_model = XGBRegressor(
        n_estimators=100,
        **xgb_params,
        subsample=0.8,
        random_state=42
    )
    eval_model.fit(X_train, y_train)
    predictions = eval_model.predict(X_test)

    comparison = test_df[["player_id", "player_name", "next_fantasy_points"]].copy()
    comparison["predicted"] = predictions
    comparison["error"] = comparison["predicted"] - comparison["next_fantasy_points"]
    comparison["absolute_error"] = comparison["error"].abs()

    return comparison

comparisons = {
    pos_name: evaluate_position_for_season(
        pos_name,
        position_dfs[pos_name],
        pos_feature_map[pos_name],
        best_final_params[pos_name],
        2024,
    )
    for pos_name in position_dfs
}

# ============================================================
# 13-15. ERROR TABLES (OVERPREDICTIONS / UNDERPREDICTIONS / LARGEST ABSOLUTE ERROR)
# ============================================================

def print_error_table(comparisons_by_position, sort_column, ascending, title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    for pos_name, comparison in comparisons_by_position.items():
        print()
        print(pos_name)
        print(
            comparison
            .sort_values(sort_column, ascending=ascending)
            [["player_name", "next_fantasy_points", "predicted", "error"]]
            .head(20)
        )

print_error_table(comparisons, "error", ascending=False, title="BIGGEST OVERPREDICTIONS")
print_error_table(comparisons, "error", ascending=True, title="BIGGEST UNDERPREDICTIONS")
print_error_table(comparisons, "absolute_error", ascending=False, title="LARGEST ABSOLUTE ERRORS")