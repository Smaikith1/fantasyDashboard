import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout='wide')

def init_state(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

def main(wrs, rbs, teams, weekly_scores, last_week_pos, point_key):
    week = weekly_scores.shape
    week = week[0]
    st.title(f'Week {week+1} Goodell Gobblers Updates')

    with st.expander('Last Week Scores'):
        col1, col2 = st.columns(2, gap='medium')

        with col1:
            st.header('Last Weeks Scores', divider=True)
            st.bar_chart(teams.iloc[:,-1].sort_values(ascending=False), horizontal=False)

        with col2:
            st.header('Last Weeks Positional Player Performance', divider=True)
            st.bar_chart(last_week_pos, stack=False)

    with st.expander('Season Totals'):

        col1, col2 = st.columns(2, gap='medium')

        with col1:
            st.header('Season Total Scores')
            st.bar_chart(teams, horizontal=False)

        with col2:
            df = pd.concat([np.sum(wrs, axis=1), np.sum(rbs, axis=1)], axis=1)
            df.columns = ['wrs', 'rbs']

            st.header('Season Total Positional Player Performance')
            st.bar_chart(df, stack=False)

    st.header('Payout Points by Week', divider=True)
    st.line_chart(weekly_scores)

    with st.expander('Points Key'):
        st.dataframe(pd.Series(point_key))