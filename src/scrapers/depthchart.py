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
    
    columns = ['C-1', 'C-2', 'C-3', '1B-1', '1B-2', '1B-3', '2B-1', '2B-2', '2B-3', 'SS-1', 'SS-2', 'SS-3', '3B-1', '3B-2', '3B-3', 'LF-1', 'LF-2', 'LF-3', 'CF-1', 'CF-2', 'CF-3', 'RF-1', 'RF-2', 'RF-3', 'DH-1', 'DH-2', 'DH-3'] # check DF existency
    
    team_name = []
    data = soup.select('tr.t-header > th > div > a > span')
    for i in data:
      t = i.text.replace(' Depth Chart','')
      team_name.append(t)
      
    dataframe_table = []
    for i in range(1,31):
      selector = 'div.col-12.before-text-margin > div > div:nth-child(' + str(i) + ') > app-single-dp-item > div > table.multi-row-data-table.t-stripped'
      table = soup.select_one(selector=selector)
      dataframe_row = []
      for a in range(3,12):
        for b in range(2,5):
          # tbody > tr:nth-child(3) > td:nth-child(2)
          selector = "tbody > tr:nth-child(" + str(a) + ") > td:nth-child(" +str(b) + ")"
          table_data = table.select_one(selector)
          if table_data:
            long_name = table_data.select_one('span.long-player-name')
            if long_name:
              dataframe_row.append(long_name.text)
            else:
              dataframe_row.append('None')
          else:
            dataframe_row.append('None')
      dataframe_table.append(dataframe_row)
    
    dp_df = pd.DataFrame(data=dataframe_table,index=LIST_TEAMS,columns=columns)
    return dp_df
  else:
    pass