import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.utils.constants import *
from src.utils.dictionaries import *

def get_team_roasters():
  batting_df = pd.DataFrame()
  pitching_df = pd.DataFrame()
  
  for i in LIST_TEAMS:
    url = URL_FGR["TEAM"]+DICT_TEAMNAMES[i][14]
    team_df = pd.read_html(url,encoding='utf-8',header=0)
    team_df = team_df[10:-1]
    team_df[0].insert(0, 'Team', i)
    team_df[1].insert(0, 'Team', i)
    batting_df = pd.concat([batting_df, team_df[0]])
    pitching_df = pd.concat([pitching_df, team_df[1]])
  
#   batting_df.to_csv('./rawfish/team_batting.csv',sep=',',encoding='utf-8')
#   pitching_df.to_csv('./rawfish/team_pitching.csv',sep=',',encoding='utf-8')
return batting_df, pitching_df

