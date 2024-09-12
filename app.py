import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

def init_state(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

def main(wrs, rbs, teams, weekly_scores, last_week_pos):
    week = weekly_scores.shape
    week = week[0]
    st.title(f'Week {week} Goodell Gobblers Updates')

    col1, col2 = st.columns(2, gap='medium')

    with col1:
        st.header('Last Weeks Scores', divider=True)
        st.bar_chart(teams.sort_values(by=teams.columns[-1], ascending=False), horizontal=False)

    with col2:
        st.header('Last Weeks Positional Player Performance', divider=True)
        st.bar_chart(last_week_pos, stack=False)

    st.header('Payout Points by Week', divider=True)
    st.line_chart(weekly_scores.T.apply(pd.to_numeric, errors='coerce'))