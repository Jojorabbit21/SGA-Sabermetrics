import pandas as pd
from pybaseball.team_batting import *
from pybaseball import team_fielding
from pybaseball.team_pitching import *
from pybaseball import team_game_logs

from src.utils.dictionaries import DICT_SOURCE, DICT_TEAMNAMES

# 각 팀 선수별 타격 지표
def get_team_batting(team, start_season=2010, end_season=2021):
    data = team_batting_bref(team, start_season, end_season)
    return data

# 각 팀별 타격지표
def get_team_batting_table(start_season=2012, end_season=2021):
    data = team_batting(start_season=start_season, end_season=end_season, league='ALL', ind=1)
    return data

# 각 팀 선수별 수비 지표
def get_team_fielding(team, start_season=2015, end_season=2021):
    data = team_fielding.team_fielding_bref(team, start_season=start_season, end_season=end_season)
    return data

# 각 팀별 수비지표 => DSR, UZR 등 추출
def get_team_fielding_table(start_season=2012, end_season=2021):
    data = team_fielding(start_season=start_season, end_season=end_season)
    return data

# 각 팀 선수별 투수지표
def get_team_pitching(team, start_season=2010, end_season=2021):
    data = team_pitching_bref(team, start_season=start_season, end_season=end_season)
    return data

# 각 팀별 투수지표 -> 318컬럼 ; 에반데
def get_team_pitching_table(start_season=2012, end_season=2021):
    data = team_pitching(start_season=start_season, end_season=end_season, league='ALL', ind=1)
    return data

# 상대전적 검색
def get_head_to_head(team, against, year:int=2021, log_type="batting"):
    team = DICT_TEAMNAMES[team][DICT_SOURCE['BBREFTEAM']]
    against = DICT_TEAMNAMES[against][DICT_SOURCE['BBREFTEAM']]
    data = team_game_logs(season=year, team=team, log_type=log_type)
    if log_type == 'batting':
        data = data[ data['Opp'] != against]
    else:
        data = data[data['Opp'] == against]
    return data