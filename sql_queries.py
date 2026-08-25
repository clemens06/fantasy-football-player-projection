import sqlite3
import pandas as pd

# Load CSVs
players_df = pd.read_csv("data/raw/players.csv", low_memory=False)

df_2018 = pd.read_csv("data/raw/stats_player_week_2018.csv", low_memory=False)
df_2019 = pd.read_csv("data/raw/stats_player_week_2019.csv", low_memory=False)
df_2020 = pd.read_csv("data/raw/stats_player_week_2020.csv", low_memory=False)
df_2021 = pd.read_csv("data/raw/stats_player_week_2021.csv", low_memory=False)
df_2022 = pd.read_csv("data/raw/stats_player_week_2022.csv", low_memory=False)
df_2023 = pd.read_csv("data/raw/stats_player_week_2023.csv", low_memory=False)
df_2024 = pd.read_csv("data/raw/stats_player_week_2024.csv", low_memory=False)

nfl_df = pd.concat(
    [df_2018, df_2019, df_2020, df_2021, df_2022, df_2023, df_2024],
    ignore_index=True
)

conn = sqlite3.connect("nfl.db")

players_df.to_sql("players", conn, if_exists="replace", index=False)
nfl_df.to_sql("weekly_stats", conn, if_exists="replace", index=False)

print("Loaded players and weekly_stats tables into nfl.db")

query = """
SELECT
    season,
    week,
    team,
    SUM(attempts) AS team_pass_attempts
FROM weekly_stats
WHERE position = 'QB'
GROUP BY season, week, team
"""

team_attempts_sql = pd.read_sql(query, conn)

print(team_attempts_sql.head(20))

conn.close()

conn = sqlite3.connect("nfl.db")

query = """
SELECT
    weekly_stats.player_id,
    weekly_stats.player_name,
    players.display_name,
    players.birth_date,
    weekly_stats.season,
    weekly_stats.week,
    weekly_stats.receiving_yards
FROM weekly_stats
LEFT JOIN players
    ON weekly_stats.player_id = players.gsis_id
WHERE weekly_stats.position = 'WR'
LIMIT 20
"""

joined_result = pd.read_sql(query, conn)

pd.set_option("display.max_columns", None)

print(joined_result)

conn.close()