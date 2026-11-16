import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NFL Game Predictor",
    page_icon="🏈",
    layout="wide"
)

st.title("🏈 NFL Game Predictor")
st.write("Compare two NFL teams using their current statistics.")

teams = {
    "Buffalo Bills": {"wins": 8, "losses": 1, "pf": 287, "pa": 199},
    "San Francisco 49ers": {"wins": 8, "losses": 1, "pf": 281, "pa": 196},
    "Chicago Bears": {"wins": 7, "losses": 2, "pf": 241, "pa": 184},
    "Cincinnati Bengals": {"wins": 7, "losses": 2, "pf": 278, "pa": 193},
    "Kansas City Chiefs": {"wins": 7, "losses": 2, "pf": 237, "pa": 156},
    "Detroit Lions": {"wins": 7, "losses": 2, "pf": 257, "pa": 199},
    "Minnesota Vikings": {"wins": 7, "losses": 2, "pf": 176, "pa": 126},
    "Denver Broncos": {"wins": 7, "losses": 2, "pf": 198, "pa": 186},
    "Jacksonville Jaguars": {"wins": 7, "losses": 2, "pf": 269, "pa": 144},
    "Pittsburgh Steelers": {"wins": 6, "losses": 3, "pf": 198, "pa": 182},
    "Cleveland Browns": {"wins": 6, "losses": 4, "pf": 188, "pa": 220},
    "Green Bay Packers": {"wins": 6, "losses": 4, "pf": 226, "pa": 221},
    "Seattle Seahawks": {"wins": 6, "losses": 4, "pf": 223, "pa": 175},
    "Los Angeles Rams": {"wins": 6, "losses": 4, "pf": 248, "pa": 187},
    "New York Giants": {"wins": 5, "losses": 3, "pf": 203, "pa": 196},
    "New England Patriots": {"wins": 5, "losses": 5, "pf": 221, "pa": 242},
    "Carolina Panthers": {"wins": 4, "losses": 5, "pf": 219, "pa": 236},
    "Dallas Cowboys": {"wins": 4, "losses": 6, "pf": 286, "pa": 282},
    "Baltimore Ravens": {"wins": 4, "losses": 5, "pf": 189, "pa": 236},
    "Las Vegas Raiders": {"wins": 4, "losses": 6, "pf": 251, "pa": 289},
    "Houston Texans": {"wins": 3, "losses": 6, "pf": 233, "pa": 219},
    "Indianapolis Colts": {"wins": 3, "losses": 7, "pf": 208, "pa": 271},
    "Tampa Bay Buccaneers": {"wins": 3, "losses": 6, "pf": 202, "pa": 178},
    "New Orleans Saints": {"wins": 3, "losses": 6, "pf": 202, "pa": 236},
    "Atlanta Falcons": {"wins": 3, "losses": 7, "pf": 201, "pa": 258},
    "Washington Commanders": {"wins": 3, "losses": 5, "pf": 196, "pa": 223},
    "Arizona Cardinals": {"wins": 3, "losses": 7, "pf": 184, "pa": 289},
    "Philadelphia Eagles": {"wins": 2, "losses": 7, "pf": 148, "pa": 221},
    "New York Jets": {"wins": 2, "losses": 8, "pf": 194, "pa": 254},
    "Miami Dolphins": {"wins": 1, "losses": 8, "pf": 148, "pa": 224},
    "Tennessee Titans": {"wins": 1, "losses": 8, "pf": 167, "pa": 239},
    "Los Angeles Chargers": {"wins": 0, "losses": 8, "pf": 121, "pa": 219},
}

home = st.selectbox("🏠 Home Team", list(teams.keys()))
away = st.selectbox(
    "✈️ Away Team",
    [team for team in teams.keys() if team != home]
)

if st.button("Predict Game", type="primary"):

    h = teams[home]
    a = teams[away]

    home_win_pct = h["wins"] / (h["wins"] + h["losses"])
    away_win_pct = a["wins"] / (a["wins"] + a["losses"])

    home_ppg = h["pf"] / (h["wins"] + h["losses"])
    away_ppg = a["pf"] / (a["wins"] + a["losses"])

    home_papg = h["pa"] / (h["wins"] + h["losses"])
    away_papg = a["pa"] / (a["wins"] + a["losses"])

    home_score = (
        home_ppg * 0.45
        + away_papg * 0.25
        + home_win_pct * 10
        + 2
    )

    away_score = (
        away_ppg * 0.45
        + home_papg * 0.25
        + away_win_pct * 10
    )

    total = home_score + away_score

    home_probability = home_score / total
    away_probability = away_score / total

    predicted_home_score = round(home_score)
    predicted_away_score = round(away_score)

    if home_probability >= away_probability:
        winner = home
    else:
        winner = away

    st.divider()

    st.subheader("🏆 Prediction")

    st.success(f"Predicted winner: **{winner}**")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            home,
            f"{home_probability * 100:.1f}%"
        )

    with col2:
        st.metric(
            away,
            f"{away_probability * 100:.1f}%"
        )

    st.subheader("Predicted Score")

    st.write(
        f"### {home} {predicted_home_score} — "
        f"{predicted_away_score} {away}"
    )

    st.subheader("Team Statistics")

    comparison = pd.DataFrame({
        "Statistic": [
            "Win %",
            "Points/Game",
            "Points Allowed/Game"
        ],
        home: [
            f"{home_win_pct * 100:.1f}%",
            f"{home_ppg:.1f}",
            f"{home_papg:.1f}"
        ],
        away: [
            f"{away_win_pct * 100:.1f}%",
            f"{away_ppg:.1f}",
            f"{away_papg:.1f}"
        ]
    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )
