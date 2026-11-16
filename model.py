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


def train_model(data):
    X = data[FEATURES]
    y = data["home_win"]

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42
    )

    model.fit(X, y)

    return model
