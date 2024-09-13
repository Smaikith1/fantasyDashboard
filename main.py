import streamlit as st
from espn_api.football import League
import numpy as np
import pandas as pd

point_key = {'Weekly Leader': 1,
             'Best Running Back Room EoY': 3,
             'Best Reciever Room EoY': 3,
             'League Winner': 15,
             'Second Place': 5,
             'Third Place': 3}

def getTables(league, point_key):
    if not hasattr(league, 'points'):
        league.rb_scores = pd.DataFrame()
        league.wr_scores = pd.DataFrame()

    rb_scores = dict()
    wr_scores = dict()
    team_scores = dict()
    weekly_accum_points = dict()

    comp_weeks = np.sum(league.teams[0].mov != 0.0)

    for wk in range(comp_weeks):
        wr_scores[wk], rb_scores[wk], team_scores[wk] = [], [], []
        if wk == 0:
            weekly_accum_points[0] = [0 for _ in range(len(league.teams))]
        else:
            weekly_accum_points[wk] = weekly_accum_points[wk-1]
        for team in league.teams:

            if not hasattr(team, 'points'):
                team.rb_scores = []
                team.wr_scores = []
                team.points = []
                team.accum_points = 0

            wrs, rbs = [], []

            for player in team.roster:
                if player.lineupSlot == 'WR':
                    wrs.append(player.total_points)
                elif player.lineupSlot == 'RB':
                    rbs.append(player.total_points)

            team.wr_scores.append(wrs)
            team.rb_scores.append(rbs)

            rb_scores[wk].append(sum(rbs))
            wr_scores[wk].append(sum(wrs))
            team_scores[wk].append(team.points_for)

        weekly_points = [i for i in team_scores[wk]]
        best_team = league.teams[weekly_points.index(max(weekly_points))]

        add_pts = []

        for ix, team in enumerate(league.teams):
            if team == best_team:
                team.points.append(point_key['Weekly Leader'])
                weekly_accum_points[wk][ix] += point_key['Weekly Leader']
            else:
                team.points.append(0)
                weekly_accum_points[wk][ix] += 0

    wr_scores = pd.DataFrame(wr_scores, index=[i.team_name for i in league.teams]).sort_values(by=comp_weeks-1, ascending=False)
    rb_scores = pd.DataFrame(rb_scores, index=[i.team_name for i in league.teams]).sort_values(by=comp_weeks-1, ascending=False)
    team_scores = pd.DataFrame(team_scores, index=[i.team_name for i in league.teams]).sort_values(by=comp_weeks-1, ascending=False)
    weekly_accum_points = pd.DataFrame(weekly_accum_points, index=[i.team_name for i in league.teams]).sort_values(by=comp_weeks-1, ascending=False)
    return wr_scores, rb_scores, team_scores, weekly_accum_points

if __name__ == '__main__':
    league_id = 94554227
    year = 2024

    league = League(league_id=league_id, year=year)

    wrs, rbs, teams, weekly_scores = getTables(league, point_key)
    lsat_week_pos = pd.concat([wrs.iloc[:,-1], rbs.iloc[:,-1]], axis=1)
    lsat_week_pos.columns = ['wrs', 'rbs']

    weekly_scores = weekly_scores.T

    for ix, _ in enumerate(weekly_scores.index):
        row = weekly_scores.iloc[ix, :]
        weekly_scores.loc[ix] = [int(i) for i in row]

    import app

    app.main(wrs, rbs, teams, weekly_scores, lsat_week_pos, point_key)