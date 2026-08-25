
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor


# ============================================================
# 1. LOAD DATA
# ============================================================

df_2018 = pd.read_csv(
    "data/raw/stats_player_week_2018.csv",
    low_memory=False
)

df_2019 = pd.read_csv(
    "data/raw/stats_player_week_2019.csv",
    low_memory=False
)

df_2020 = pd.read_csv(
    "data/raw/stats_player_week_2020.csv",
    low_memory=False
)

df_2021 = pd.read_csv(
    "data/raw/stats_player_week_2021.csv",
    low_memory=False
)

df_2022 = pd.read_csv(
    "data/raw/stats_player_week_2022.csv",
    low_memory=False
)

df_2023 = pd.read_csv(
    "data/raw/stats_player_week_2023.csv",
    low_memory=False
)

df_2024 = pd.read_csv(
    "data/raw/stats_player_week_2024.csv",
    low_memory=False
)

players_df = pd.read_csv(
    "data/raw/players.csv",
    low_memory=False
)

print("\nPlayer data:")
print(players_df.columns)
print(players_df.head())


# Combine NFL data

nfl_df = pd.concat(
    [df_2018, df_2019, df_2020, df_2021, df_2022, df_2023, df_2024],
    ignore_index=True
)

print(
    [
        col for col in nfl_df.columns
        if "team" in col.lower()
    ]
)


# Only regular season

nfl_df = nfl_df[
    nfl_df["season_type"] == "REG"
].copy()

print("Dataset shape:", nfl_df.shape)


# ============================================================
# 2. FILTER TO WRs
# ============================================================

wr_df = nfl_df[
    nfl_df["position"] == "WR"
].copy()

print("WR rows:", wr_df.shape)

# Sum team pass attempts per week, from QB rows in the full weekly dataset
team_attempts = (
    nfl_df[nfl_df["position"] == "QB"]
    .groupby(["season", "week", "team"])["attempts"]
    .sum()
    .reset_index()
    .rename(columns={"attempts": "team_pass_attempts"})
)

# Merge onto the weekly WR data using season, week, and team
wr_df = wr_df.merge(
    team_attempts,
    on=["season", "week", "team"],
    how="left"
)

# ============================================================
# 3. CREATE SEASON-LEVEL WR DATA
# ============================================================

# IMPORTANT:
# Group by player_id, NOT player_name.
#
# player_id is the actual identity of the player.
# This prevents cases like Nathaniel "Tank" Dell appearing
# as N.Dell and T.Dell from becoming separate players.

wr_season = (
    wr_df
    .groupby(
        ["season", "player_id"]
    )
    .agg(
        games=("game_id", "nunique"),
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

print(wr_df[["season", "week", "team", "team_pass_attempts"]].head(20))

# ============================================================
# 4. ADD OFFICIAL PLAYER INFORMATION + AGE
# ============================================================

player_data = players_df[
    [
        "gsis_id",
        "display_name",
        "birth_date"
    ]
].copy()

player_data["birth_date"] = pd.to_datetime(
    player_data["birth_date"],
    errors="coerce"
)

# Merge player information

wr_season = wr_season.merge(
    player_data,
    left_on="player_id",
    right_on="gsis_id",
    how="left"
)


# Remove duplicate ID column

wr_season = wr_season.drop(
    columns=["gsis_id"]
)


# Rename official name to player_name

wr_season = wr_season.rename(
    columns={
        "display_name": "player_name"
    }
)


# Calculate age at end of season

season_end = pd.to_datetime(
    wr_season["season"].astype(str) + "-12-31"
)

wr_season["age"] = (
    season_end
    - wr_season["birth_date"]
).dt.days / 365.25


print()
print("Age check:")

print(
    wr_season[
        [
            "player_name",
            "season",
            "birth_date",
            "age"
        ]
    ].head(20)
)


# ============================================================
# 5. PLAYER IDENTITY CHECK
# ============================================================

print()
print("=" * 60)
print("PLAYER IDENTITY CHECK")
print("=" * 60)


duplicate_player_seasons = (
    wr_season
    .duplicated(
        subset=[
            "season",
            "player_id"
        ],
        keep=False
    )
)


print(
    "Duplicate player-seasons:",
    duplicate_player_seasons.sum()
)


print(
    wr_season[
        duplicate_player_seasons
    ]
    .sort_values(
        ["player_id", "season"]
    )
)


# ============================================================
# 6. TANK DELL CHECK
# ============================================================

print()
print("TANK DELL CHECK:")

print(
    wr_season[
        wr_season["player_id"] == "00-0038977"
    ][
        [
            "player_id",
            "player_name",
            "season",
            "games",
            "targets",
            "receptions",
            "receiving_yards",
            "fantasy_points_ppr"
        ]
    ]
    .sort_values("season")
)


# ============================================================
# 7. CREATE FEATURES
# ============================================================

wr_season["targets_per_game"] = (
    wr_season["targets"]
    / wr_season["games"]
)

wr_season["receptions_per_game"] = (
    wr_season["receptions"]
    / wr_season["games"]
)

wr_season["yards_per_game"] = (
    wr_season["receiving_yards"]
    / wr_season["games"]
)

wr_season["catch_rate"] = (
    wr_season["receptions"]
    / wr_season["targets"]
)

wr_season["yards_per_target"] = (
    wr_season["receiving_yards"]
    / wr_season["targets"]
)

wr_season["yards_per_reception"] = (
    wr_season["receiving_yards"]
    / wr_season["receptions"]
)

wr_season["fantasy_points_per_game"] = (
    wr_season["fantasy_points_ppr"]
    / wr_season["games"]
)

wr_season["target_share"] = (
    wr_season["targets"] / wr_season["team_pass_attempts"]
)

wr_season["target_share"] = wr_season["target_share"].replace(
    [float("inf"), -float("inf")], 0
).fillna(0)

# Replace undefined ratios with 0

ratio_columns = [
    "targets_per_game",
    "receptions_per_game",
    "yards_per_game",
    "catch_rate",
    "yards_per_target",
    "yards_per_reception",
    "fantasy_points_per_game"
]

wr_season[ratio_columns] = (
    wr_season[ratio_columns]
    .replace(
        [float("inf"), -float("inf")],
        0
    )
    .fillna(0)
)


# ============================================================
# 8. CREATE NEXT-SEASON TARGET
# ============================================================

wr_season["next_season"] = (
    wr_season["season"] + 1
)


future = wr_season[
    [
        "season",
        "player_id",
        "fantasy_points_ppr"
    ]
].copy()


future = future.rename(
    columns={
        "season": "next_season",
        "fantasy_points_ppr":
            "next_fantasy_points"
    }
)


model_df = wr_season.merge(
    future,
    on=[
        "next_season",
        "player_id"
    ],
    how="inner"
)


# Previous-season fantasy points

model_df["previous_fantasy_points"] = (
    model_df["fantasy_points_ppr"]
)


print()
print("Model rows by season:")

print(
    model_df
    .groupby("season")
    .size()
)


# ============================================================
# 9. DEFINE FEATURES
# ============================================================

features = [
    "targets",
    "receptions",
    "receiving_yards",
    "receiving_tds",
    "games",
    "targets_per_game",
    "receptions_per_game",
    "yards_per_game",
    "previous_fantasy_points",
    "catch_rate",
    "yards_per_target",
    "yards_per_reception",
    "fantasy_points_per_game",
    "age",
    "target_share"
]


# ============================================================
# 10. CROSS-SEASON MODEL VALIDATION
# ============================================================

print()
print("=" * 60)
print("CROSS-SEASON MODEL VALIDATION")
print("=" * 60)


validation_results = []


for prediction_season in [2020, 2021, 2022, 2023, 2024]:
    train_df = model_df[model_df["next_season"] < prediction_season]
    test_df = model_df[model_df["next_season"] == prediction_season]

    X_train = train_df[features]
    y_train = train_df[
        "next_fantasy_points"
    ]

    X_test = test_df[features]
    y_test = test_df[
        "next_fantasy_points"
    ]


    print()
    print(
        f"Predicting: {prediction_season}"
    )

    print(
        "Training:",
        X_train.shape
    )

    print(
        "Testing:",
        X_test.shape
    )


    # --------------------------------------------------------
    # Linear Regression
    # --------------------------------------------------------

    linear_model = LinearRegression()

    linear_model.fit(
        X_train,
        y_train
    )

    linear_predictions = (
        linear_model.predict(X_test)
    )

    linear_mae = mean_absolute_error(
        y_test,
        linear_predictions
    )


    print(
        "Linear Regression MAE:",
        round(linear_mae, 2)
    )


    # --------------------------------------------------------
    # Baseline
    # --------------------------------------------------------

    baseline_predictions = (
        test_df[
            "previous_fantasy_points"
        ]
    )


    baseline_mae = mean_absolute_error(
        y_test,
        baseline_predictions
    )


    print(
        "Baseline MAE:",
        round(baseline_mae, 2)
    )


    # --------------------------------------------------------
    # Random Forest
    # --------------------------------------------------------

    rf_model = RandomForestRegressor(
        n_estimators=300,
        max_depth=8,
        random_state=42
    )


    rf_model.fit(
        X_train,
        y_train
    )


    rf_predictions = (
        rf_model.predict(X_test)
    )


    rf_mae = mean_absolute_error(
        y_test,
        rf_predictions
    )


    print(
        "Random Forest MAE:",
        round(rf_mae, 2)
    )


    validation_results.append({
        "season": prediction_season,
        "linear_mae": linear_mae,
        "baseline_mae": baseline_mae,
        "random_forest_mae": rf_mae
    })


# ============================================================
# 11. RANDOM FOREST FEATURE IMPORTANCE
# ============================================================

print()
print("=" * 60)
print("RANDOM FOREST FEATURE IMPORTANCE")
print("=" * 60)


final_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=8,
    random_state=42
)


final_model.fit(
    model_df[features],
    model_df["next_fantasy_points"]
)


feature_importance = pd.DataFrame({
    "feature": features,
    "importance":
        final_model.feature_importances_
})


feature_importance = (
    feature_importance
    .sort_values(
        "importance",
        ascending=False
    )
)


print(feature_importance)


# ============================================================
# 12. MISSING VALUES
# ============================================================

print()
print("=" * 60)
print("MISSING VALUES")
print("=" * 60)


print(
    model_df[features]
    .isna()
    .sum()
)


# ============================================================
# 13. MODEL SUMMARY
# ============================================================

print()
print("=" * 60)
print("MODEL COMPLETE")
print("=" * 60)


print(
    f"Training rows: {len(model_df)}"
)

print(
    f"Features: {len(features)}"
)

print(
    "Best model so far: Random Forest"
)


# ============================================================
# 14. PLAYER DATA CHECK
# ============================================================

print()

print(
    nfl_df[
        [
            "player_id",
            "player_name"
        ]
    ]
    .drop_duplicates()
    .head(20)
)

print(
    nfl_df["player_id"].dtype
)


print(
    nfl_df[
        [
            "player_id",
            "player_name",
            "player_display_name"
        ]
    ]
    .drop_duplicates()
    .head(30)
)


print(
    "\nUnique players:",
    nfl_df["player_id"].nunique()
)


# ============================================================
# 15. GENERATE 2025 WR PROJECTIONS
# ============================================================

print()
print("=" * 60)
print("2025 WR PROJECTIONS")
print("=" * 60)


# Train final model on all historical examples

final_model = RandomForestRegressor(
    n_estimators=500,
    max_depth=8,
    random_state=42
)


final_model.fit(
    model_df[features],
    model_df["next_fantasy_points"]
)


# Get 2024 WRs

projection_df = wr_season[
    wr_season["season"] == 2024
].copy()


projection_df[
    "previous_fantasy_points"
] = (
    projection_df[
        "fantasy_points_ppr"
    ]
)


# Fill missing ages

projection_df["age"] = (
    projection_df["age"]
    .fillna(
        projection_df["age"].median()
    )
)


# Generate projections

projection_df[
    "projected_fantasy_points"
] = final_model.predict(
    projection_df[features]
)


# Sort projections

projection_df = (
    projection_df
    .sort_values(
        "projected_fantasy_points",
        ascending=False
    )
)


print()
print(
    "Top 50 WR Projections for 2025:"
)

print()


print(
    projection_df[
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
    .head(50)
    .to_string(index=False)
)


# ============================================================
# 16. GAME COUNT CHECK
# ============================================================

print()

print(
    wr_df
    .groupby(
        [
            "season",
            "player_id",
            "player_name"
        ]
    )["game_id"]
    .nunique()
    .sort_values(
        ascending=False
    )
    .head(20)
)


print(
    wr_df[
        "season_type"
    ].value_counts()
)


# ============================================================
# 17. 2024 MODEL ERROR ANALYSIS
# ============================================================

# Recreate 2024 test set explicitly

train_df = model_df[
    model_df["next_season"] < 2024
]

test_df = model_df[
    model_df["next_season"] == 2024
]


X_train = train_df[features]

y_train = train_df[
    "next_fantasy_points"
]

X_test = test_df[features]

y_test = test_df[
    "next_fantasy_points"
]


# Train 2024 evaluation model

rf_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=8,
    random_state=42
)


rf_model.fit(
    X_train,
    y_train
)


predictions = rf_model.predict(
    X_test
)


comparison = test_df[
    [
        "player_id",
        "player_name",
        "next_fantasy_points"
    ]
].copy()


comparison["predicted"] = predictions


comparison["error"] = (
    comparison["predicted"]
    - comparison["next_fantasy_points"]
)


comparison["absolute_error"] = (
    comparison["error"].abs()
)


# ============================================================
# 18. BIGGEST OVERPREDICTIONS
# ============================================================

print()
print("=" * 60)
print("BIGGEST OVERPREDICTIONS")
print("=" * 60)


print(
    comparison
    .sort_values(
        "error",
        ascending=False
    )[
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
# 19. BIGGEST UNDERPREDICTIONS
# ============================================================

print()
print("=" * 60)
print("BIGGEST UNDERPREDICTIONS")
print("=" * 60)


print(
    comparison
    .sort_values(
        "error"
    )[
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
# 20. LARGEST ABSOLUTE ERRORS
# ============================================================

print()
print("=" * 60)
print("LARGEST ABSOLUTE ERRORS")
print("=" * 60)


print(
    comparison
    .sort_values(
        "absolute_error",
        ascending=False
    )[
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
# 21. DUPLICATE CHECK ON 2024 TEST SET
# ============================================================

print()
print("=" * 60)
print("2024 TEST SET DUPLICATE CHECK")
print("=" * 60)


print(
    "Rows:",
    len(comparison)
)

print(
    "Unique player IDs:",
    comparison["player_id"].nunique()
)


duplicates = comparison[
    comparison["player_id"].duplicated(
        keep=False
    )
]


print(
    "Duplicate player IDs:"
)

print(
    duplicates
    .sort_values("player_id")
)


# ============================================================
# 22. PROBLEM PLAYER CHECK
# ============================================================

problem_ids = [
    "00-0035216",
    "00-0037240",
    "00-0038977"
]


print()
print("=" * 60)
print("PROBLEM PLAYER CHECK")
print("=" * 60)


print(
    wr_season[
        wr_season["player_id"]
        .isin(problem_ids)
    ][
        [
            "player_id",
            "player_name",
            "season",
            "games",
            "targets",
            "receptions",
            "receiving_yards",
            "fantasy_points_ppr"
        ]
    ]
    .sort_values(
        [
            "player_id",
            "season"
        ]
    )
)

print(nfl_df.columns)