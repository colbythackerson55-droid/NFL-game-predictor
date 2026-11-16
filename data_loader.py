import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/nflverse/nfldata/master/data/games.csv"


def load_games():
    df = pd.read_csv(DATA_URL)

    # Only completed regular-season games
    df = df[
        (df["game_type"] == "REG") &
        (df["home_score"].notna()) &
        (df["away_score"].notna())
    ].copy()

    df["home_win"] = (
        df["home_score"] > df["away_score"]
    ).astype(int)

    return df
