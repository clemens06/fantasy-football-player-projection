

# This is a test file for calculating fantasy points for NFL players based on their stats.

players = [

    {
        "name": "Ja'Marr Chase",
        "team": "CIN",
        "position": "WR",
        "targets": 12,
        "receptions": 8,
        "receiving_yards": 120,
        "receiving_touchdowns": 2
    },

    {
        "name": "Amon-Ra St. Brown",
        "team": "DET",
        "position": "WR",
        "targets": 16,
        "receptions": 15,
        "receiving_yards": 110,
        "receiving_touchdowns": 1
    },

    {
        "name": "Jameson Williams",
        "team": "DET",
        "position": "WR",
        "targets": 6,
        "receptions": 4,
        "receiving_yards": 143,
        "receiving_touchdowns": 2
    }

]

# function to calculate fantasy points for a player based on their stats
def calculate_fantasy_points(player):

    fantasy_points = (
        player["receiving_yards"] * 0.1
        + player["receptions"] * 1
        + player["receiving_touchdowns"] * 6
    )

    return fantasy_points

#for each player in the players list, calculate their fantasy points and print their name and points
for player in players:

    points = calculate_fantasy_points(player)

    print(player["name"], points)

import pandas as pd

#create a DataFrame from the players list
data = {
    "name": ["Ja'Marr Chase", "Amon-Ra St. Brown", "Jameson Williams"],
    "team": ["CIN", "DET", "DET"],
    "position": ["WR", "WR", "WR"],
    "targets": [12, 16, 6],
    "receptions": [8, 15, 4],
    "receiving_yards": [120, 110, 143],
    "receiving_touchdowns": [2, 1, 2]
}

messy_data = {
    "name": ["Ja'Marr Chase", "Amon-Ra St. Brown", "Jameson Williams", None],
    "targets": [12, 16, 6, 10],
    "receiving_yards": [120, 110, 143, None]
}

messy_df = pd.DataFrame(messy_data)

print(messy_df)

# #create a DataFrame from the data
# df = pd.DataFrame(data)

# #calculate fantasy points for each player and add it as a new column in the DataFrame
# df["fantasy_points"] = (
#     df["receiving_yards"] * 0.1
#     + df["receptions"] * 1
#     + df["receiving_touchdowns"] * 6
# )

# #print the top 2 players based on fantasy points, can do for any number, for example targets, receptions, etc. head = top, tail = bottom
# print(df.sort_values("fantasy_points", ascending=False).head(2))

# #print the average fantasy points for each player- can do by any string column, in this case "name"
# print(df.groupby("name")["fantasy_points"].mean())


# print(df.describe())


# print whether there is any missing info in the DataFrame, can do for any column, for example targets, receptions, etc.
print(messy_df.isnull())

# print the sum of missing info in each column, can do for any column, for example targets, receptions, etc.
print(messy_df.isnull().sum())

# drop any rows with missing info, can do for any column, for example targets, receptions, etc.
clean_df = messy_df.dropna()

# print the cleaned DataFrame
print(clean_df)


df = pd.read_csv("players.csv")

print(df)