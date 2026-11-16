
import streamlit as st
import pandas as pd

INJURY_URL = (
    "https://github.com/nflverse/nfldata/"
    "releases/download/injuries/injuries_2026.csv"
)

TEAM_CODES = {
    "Buffalo Bills": "BUF",
    "Kansas City Chiefs": "KC",
    "Philadelphia Eagles": "PHI",
    "Dallas Cowboys": "DAL",
    "Detroit Lions": "DET",
    "San Francisco 49ers": "SF",
    "Carolina Panthers": "CAR",
    "Pittsburgh Steelers": "PIT",
    "New York Jets": "NYJ",
    "Miami Dolphins": "MIA",
}

@st.cache_data(ttl=3600)
def load_injuries():
    try:
        df = pd.read_csv(INJURY_URL)
        return df
    except Exception as error:
        st.error("Could not load injury data.")
        st.exception(error)
        return None
def show_injuries(home_team, away_team):

    st.header("🏥 Injury Report")

    try:
        injuries = load_injuries()

        teams = [
            TEAM_CODES[home_team],
            TEAM_CODES[away_team]
        ]

        filtered = injuries[
            injuries["team"].isin(teams)
        ].copy()

        filtered = filtered.sort_values(
            "week", ascending=False
        )

        for team_name, team_code in [
            (home_team, TEAM_CODES[home_team]),
            (away_team, TEAM_CODES[away_team])
        ]:

            st.subheader(team_name)

            team_injuries = filtered[
                filtered["team"] == team_code
            ]

            if team_injuries.empty:
                st.info("No injury entries found.")
                continue

            display = team_injuries[[
                "full_name",
                "position",
                "report_primary_injury",
                "practice_status",
                "report_status",
                "week"
            ]].rename(columns={
                "full_name": "Player",
                "position": "Position",
                "report_primary_injury": "Injury",
                "practice_status": "Practice",
                "report_status": "Game Status",
                "week": "Week"
            })

            st.dataframe(
                display,
                use_container_width=True,
                hide_index=True
            )

        st.caption(
            "Source: nflverse. Data refreshes every hour "
            "in this app; source data updates daily."
        )

except Exception as error:
    st.error("Injury data loading failed:")
    st.exception(error)

