import streamlit as st

st.set_page_config(
    page_title="NFL Game Predictor",
    page_icon="🏈"
)

st.title("🏈 NFL Game Predictor")
st.write("Predict the winner of an NFL matchup.")

st.header("Home Team")

home_team = st.text_input("Home team", "Buffalo Bills")
home_strength = st.slider("Home team strength", 0, 100, 75)

st.header("Away Team")

away_team = st.text_input("Away team", "Kansas City Chiefs")
away_strength = st.slider("Away team strength", 0, 100, 70)

if st.button("Predict Game"):
    total = home_strength + away_strength

    home_probability = home_strength / total
    away_probability = away_strength / total

    if home_probability > away_probability:
        winner = home_team
    else:
        winner = away_team

    st.success(f"Predicted winner: {winner}")

    st.write(
        f"**{home_team}:** {home_probability * 100:.1f}%"
    )

    st.write(
        f"**{away_team}:** {away_probability * 100:.1f}%"
    )
