import streamlit as st
import pandas as pd

def show_injuries():

    st.header("🏥 NFL Injury Tracker")

    st.write(
        "Enter player availability information "
        "to keep track of team injuries."
    )

    teams = [
        "Buffalo Bills",
        "Kansas City Chiefs",
        "Philadelphia Eagles",
        "Dallas Cowboys",
        "Detroit Lions",
        "San Francisco 49ers",
        "Carolina Panthers",
        "Pittsburgh Steelers",
        "New York Jets",
        "Miami Dolphins"
    ]

    with st.form("injury_form"):

        player = st.text_input("Player name")

        team = st.selectbox("Team", teams)

        position = st.selectbox(
            "Position",
            ["QB", "RB", "WR", "TE", "OL",
             "DL", "LB", "CB", "S", "K"]
        )

        injury = st.text_input("Injury")

        status = st.selectbox(
            "Game status",
            ["Out", "Doubtful", "Questionable",
             "Available", "Not reported"]
        )

        submitted = st.form_submit_button(
            "Add Player"
        )

    if "injuries" not in st.session_state:
        st.session_state.injuries = []

    if submitted and player:
        st.session_state.injuries.append({
            "Player": player,
            "Team": team,
            "Position": position,
            "Injury": injury,
            "Status": status
        })

    if st.session_state.injuries:

        df = pd.DataFrame(
            st.session_state.injuries
        )

        st.subheader("Current Injury List")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.write(
            "Players listed:",
            len(df)
        )
