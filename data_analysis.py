import pandas as pd

df = pd.read_csv("players.csv")

df.info()
df["catch_rate"] = df["receptions"] / df["targets"]

df["yards_per_reception"] = df["receiving_yards"] / df["receptions"]

df["yards_per_target"] = df["receiving_yards"] / df["targets"]

df["fantasy_points"] = (
    df["receiving_yards"] * 0.1
    + df["receptions"] * 1
    + df["receiving_touchdowns"] * 6
)

X = df[["targets", "receptions", "receiving_yards", "receiving_touchdowns"]]

y = df["fantasy_points"]

nfl_df = pd.read_csv("data/raw/stats_player_week_2024.csv")

print(nfl_df.shape)
print(nfl_df.columns)