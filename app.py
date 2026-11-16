from injuries import show_injuries
import streamlit as st
import pandas as pd

from data_loader import load_games
from model import create_training_data, train_model, FEATURES


st.set_page_config(
    page_title="NFL Game Predictor",
    page_icon="🏈",
    layout="wide"
)

st.title("🏈 NFL Game Predictor")
st.write("Machine-learning predictions based on historical NFL game data.")


@st.cache_data
def get_training_data():
    games = load_games()
    return create_training_data(games)


@st.cache_resource
def get_model():
    training_data = get_training_data()
    return train_model(training_data)


try:
    training_data = get_training_data()
    model = get_model()

    st.success(
        f"Model trained using {len(training_data):,} historical games."
    )

except Exception as e:
    st.error("The model could not be loaded.")
    st.exception(e)
    st.stop()


teams = sorted(
    set(
        training_data.index
        if False
        else []
    )
)

# NFL teams currently appearing in the historical dataset
games = load_games()

teams = sorted(
    set(games["home_team"].unique()) |
    set(games["away_team"].unique())
)


col1, col2 = st.columns(2)

with col1:
    home_team = st.selectbox(
        "🏠 Home Team",
        teams
    )

with col2:
    away_options = [
        team for team in teams
        if team != home_team
    ]

    away_team = st.selectbox(
        "✈️ Away Team",
        away_options
    )


if st.button("Predict Game", type="primary"):

    # Calculate current statistics from the historical dataset
    team_stats = {}

    for team in teams:
        team_games = games[
            (games["home_team"] == team) |
            (games["away_team"] == team)
        ]

        wins = 0
        points = 0
        allowed = 0

        for _, game in team_games.iterrows():

            if game["home_team"] == team:
                points += game["home_score"]
                allowed += game["away_score"]

                if game["home_score"] > game["away_score"]:
                    wins += 1

            else:
                points += game["away_score"]
                allowed += game["home_score"]

                if game["away_score"] > game["home_score"]:
                    wins += 1

        number_of_games = len(team_games)

        if number_of_games > 0:
            team_stats[team] = {
                "win_pct": wins / number_of_games,
                "ppg": points / number_of_games,
                "papg": allowed / number_of_games
            }

    home = team_stats[home_team]
    away = team_stats[away_team]

    prediction = pd.DataFrame([{
        "home_win_pct": home["win_pct"],
        "away_win_pct": away["win_pct"],
        "home_ppg": home["ppg"],
        "away_ppg": away["ppg"],
        "home_papg": home["papg"],
        "away_papg": away["papg"]
    }])

    prediction = prediction[FEATURES]

    probabilities = model.predict_proba(prediction)[0]

    away_probability = probabilities[0]
    home_probability = probabilities[1]

    if home_probability >= away_probability:
        winner = home_team
    else:
        winner = away_team

    st.divider()

    st.subheader("🏆 Prediction")

    st.success(f"Predicted winner: **{winner}**")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            home_team,
            f"{home_probability * 100:.1f}%"
        )

    with c2:
        st.metric(
            away_team,
            f"{away_probability * 100:.1f}%"
        )

    st.subheader("📊 Team Statistics")

    comparison = pd.DataFrame({
        "Statistic": [
            "Win Percentage",
            "Points Per Game",
            "Points Allowed Per Game"
        ],
        home_team: [
            f"{home['win_pct'] * 100:.1f}%",
            f"{home['ppg']:.1f}",
            f"{home['papg']:.1f}"
        ],
        away_team: [
            f"{away['win_pct'] * 100:.1f}%",
            f"{away['ppg']:.1f}",
            f"{away['papg']:.1f}"
        ]
    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

