import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor


df_2021 = pd.read_csv("data/raw/stats_player_week_2021.csv")
df_2022 = pd.read_csv("data/raw/stats_player_week_2022.csv")
df_2023 = pd.read_csv("data/raw/stats_player_week_2023.csv")
df_2024 = pd.read_csv("data/raw/stats_player_week_2024.csv")

nfl_df = pd.concat(
    [df_2021, df_2022, df_2023, df_2024],
    ignore_index=True
)

print(nfl_df.shape)
print(nfl_df.columns)

print(nfl_df[["player_name", "position", "season", "week", "fantasy_points"]].head(20))

skill_positions = ["QB", "RB", "WR", "TE"]

skill_df = nfl_df[nfl_df["position"].isin(skill_positions)]

print(skill_df.shape)
print(skill_df["position"].value_counts())

wr_df = nfl_df[nfl_df["position"] == "WR"]

print(wr_df.shape)

print(
    wr_df[
        [
            "player_name",
            "season",
            "week",
            "targets",
            "receptions",
            "receiving_yards",
            "receiving_tds",
            "fantasy_points",
            "fantasy_points_ppr"
        ]
    ].head(20)
)

wr_season = (
    wr_df
    .groupby(["season", "player_id", "player_name"])
    .agg(
        games=("game_id", "nunique"),
        targets=("targets", "sum"),
        receptions=("receptions", "sum"),
        receiving_yards=("receiving_yards", "sum"),
        receiving_tds=("receiving_tds", "sum"),
        fantasy_points=("fantasy_points", "sum"),
        fantasy_points_ppr=("fantasy_points_ppr", "sum")
    )
    .reset_index()
)

wr_season["targets_per_game"] = (
    wr_season["targets"] / wr_season["games"]
)

wr_season["receptions_per_game"] = (
    wr_season["receptions"] / wr_season["games"]
)

wr_season["yards_per_game"] = (
    wr_season["receiving_yards"] / wr_season["games"]
)

wr_season["next_season"] = wr_season["season"] + 1

future = wr_season[
    ["season", "player_id", "fantasy_points_ppr"]
].copy()

future = future.rename(
    columns={
        "season": "next_season",
        "fantasy_points_ppr": "next_fantasy_points"
    }
)

model_df = wr_season.merge(
    future,
    on=["next_season", "player_id"],
    how="inner"
)

print("\nModel rows by season:")
print(model_df.groupby("season").size())

features = [
    "targets",
    "receptions",
    "receiving_yards",
    "receiving_tds",
    "games",
    "targets_per_game",
    "receptions_per_game",
    "yards_per_game"
]

train_df = model_df[model_df["season"] < 2023]
test_df = model_df[model_df["season"] == 2023]

X_train = train_df[features]
y_train = train_df["next_fantasy_points"]

X_test = test_df[features]
y_test = test_df["next_fantasy_points"]

print("Training:", X_train.shape)
print("Testing:", X_test.shape)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

print("MAE:", mae)

rf_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=8,
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_predictions = rf_model.predict(X_test)

rf_mae = mean_absolute_error(y_test, rf_predictions)

print("Random Forest MAE:", rf_mae)