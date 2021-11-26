import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep

from src.utils.constants import *
from src.utils.dictionaries import *

# 팀 투수, 타자 리스트를 뽑고 간단한 스탯을 불러온다.
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


# 팀 포지션 별 뎁스차트를 불러온다.
def get_team_depthcharts():
  headers={'User-Agent':USER_AGENT}
  r = requests.get(URL_LINEUPS['DC'], headers=headers)
  r.encoding='utf-8'
  if r.status_code == 200:
    html = r.text
    soup = BeautifulSoup(html, 'lxml')

    columns = ['POS', '1', '2', '3']
    index = ['C', '1B', '2B', 'SS', '3B', 'LF', 'CF', 'RF', 'DH'] # check DF existency
    
    team_name = []
    data = soup.select('tr.t-header > th > div > a > span')
    for i in data:
      t = i.text.replace(' Depth Chart','')
      team_name.append(t)
    
    # body > app-root > div.outlet-container > app-depth-charts > div > div > div.col-12.before-text-margin > div > div:nth-child(1) > app-single-dp-item > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > app-player-link > a > span > span.long-player-name
                                                                                                                  # nth-child 팀 선택 1~30                                      tr:nth-child(3-10) #DH는 11