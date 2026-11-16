import pandas as pd
from sklearn.ensemble import RandomForestClassifier

FEATURES = [
    "home_win_pct",
    "away_win_pct",
    "home_ppg",
    "away_ppg",
    "home_papg",
    "away_papg",
]


def create_training_data(games):
    games = games.sort_values("gameday").copy()

    team_stats = {}

    rows = []

    for _, game in games.iterrows():
        home = game["home_team"]
        away = game["away_team"]

        if home not in team_stats:
            team_stats[home] = {
                "wins": 0,
                "games": 0,
                "points": 0,
                "allowed": 0
            }

        if away not in team_stats:
            team_stats[away] = {
                "wins": 0,
                "games": 0,
                "points": 0,
                "allowed": 0
            }

        h = team_stats[home]
        a = team_stats[away]

        # Only use information available BEFORE this game.
        if h["games"] > 0 and a["games"] > 0:
            rows.append({
                "home_win_pct": h["wins"] / h["games"],
                "away_win_pct": a["wins"] / a["games"],
                "home_ppg": h["points"] / h["games"],
                "away_ppg": a["points"] / a["games"],
                "home_papg": h["allowed"] / h["games"],
                "away_papg": a["allowed"] / a["games"],
                "home_win": int(game["home_score"] > game["away_score"])
            })

        # Update statistics AFTER the game.
        h["games"] += 1
        a["games"] += 1

        h["points"] += game["home_score"]
        h["allowed"] += game["away_score"]

        a["points"] += game["away_score"]
        a["allowed"] += game["home_score"]

        if game["home_score"] > game["away_score"]:
            h["wins"] += 1
        else:
            a["wins"] += 1

    return pd.DataFrame(rows)


def train_model(training_data):
    X = training_data[FEATURES]
    y = training_data["home_win"]

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42
    )

    model.fit(X, y)

    return model
