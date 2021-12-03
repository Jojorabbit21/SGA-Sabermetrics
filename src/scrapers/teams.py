from numpy import log
import pandas as pd
import datetime
import chromedriver_autoinstaller
from time import sleep, time
from pybaseball.team_batting import *
from pybaseball import team_fielding
from pybaseball.team_pitching import *
from pybaseball import team_game_logs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.utils.constants import *
from src.utils.dictionaries import *
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

  return batting_df, pitching_df

def get_batting_leaderboard(team, start_season=2010, end_season=2021):
    data = team_batting_bref(team, start_season, end_season)
    return data

def get_team_batting_table(start_season=2015, end_season=2021):
    data = team_batting(start_season=start_season, end_season=end_season, league='ALL', ind=1, split_seasons=False)
    data.sort_values(by='Team',axis=0, ascending=True, inplace=True)
    data = data.drop(['teamIDfg', 'Age'], axis=1)
    # data = data.drop(['teamIDfg', 'Season', 'Age'], axis=1)
    data.reset_index(inplace=True, drop=True)
    return data

def get_fielding_leaderboard(team, start_season=2015, end_season=2021):
    data = team_fielding.team_fielding_bref(team, start_season=start_season, end_season=end_season)
    return data

def get_team_fielding_table(start_season=2012, end_season=2021):
    data = pd.read_html(URL_FGR['TEAM_FIELDING'])
    data = data[-2:-1][0]
    data = data['1  Page size:  select  30 items in 1 pages']
    for i in range(len(data)):
        teamname = data.loc[[i],['Team']].to_numpy()
        teamname = str(teamname[0][0])
        if teamname != '1  Page size:  select  30 items in 1 pages':
            teamname = DICT_BP_LINEUP[teamname]
        data.loc[[i],['Team']] = teamname
    data = data.drop([data.index[30]],axis=0)
    data = data.drop(['#'], axis=1)
    data.sort_values(by='Team',axis=0, ascending=True, inplace=True)
    data.reset_index(inplace=True, drop=True)
    return data

def get_pitching_leaderboard(team, start_season=2010, end_season=2021):
    data = team_pitching_bref(team, start_season=start_season, end_season=end_season)
    return data

def get_team_pitching_table(start_season=2018, end_season=2021):
    data = pd.DataFrame(index=range(0,30))
    for i in range(3):
        series = pd.read_html(URL_FGR['TEAM_PITCHING'][i])
        series = series[-2:-1][0] 
        series = series['1  Page size:  select  30 items in 1 pages']
        series = series.drop([series.index[30]],axis=0)
        series.sort_values(by=['Team'],axis=0,ascending=[True],inplace=True)
        if i == 0:
            series = series.drop('#', axis=1)
        if i == 1 or i == 2:
            series = series.drop(['#','Team'],axis=1)
        data = pd.concat([data, series], axis=1)
    data.sort_values(by='Team',axis=0, ascending=True, inplace=True)
    data.reset_index(inplace=True, drop=True)
    return data

def get_head_to_head(team, against, year:int=2021, log_type="batting"):
    team = DICT_TEAMNAMES[team][DICT_SOURCE['BBREFTEAM']]
    against = DICT_TEAMNAMES[against][DICT_SOURCE['BBREFTEAM']]
    data = team_game_logs(season=year, team=team, log_type=log_type)
    data_opp = team_game_logs(season=year, team=against, log_type=log_type)
    
    # Sanitize DataFrame
    debris = data[ data['Opp'] != against ].index
    if len(debris) > 0:
        data.drop(debris, inplace=True)
        data = data.reset_index(drop=True)
    date = data['Date']
    home = data['Home']
    opp = data['Opp']
    result = data['Rslt']
    data.drop(['Game','Date','Home','Opp','Rslt','PitchersUsed'], axis=1, inplace=True)
    data = data.reset_index(drop=True)
    header = pd.DataFrame(index=range(0,len(home)), columns = ['Date', 'Visitor','Home','Result','Score'])
    for i in range(len(home)):
        header.loc[[i],['Date']] = date[i]
        if home[i] == True:
            header.loc[[i],['Visitor']] = opp[i]
            header.loc[[i],['Home']] = team
        else:
            header.loc[[i],['Visitor']] = team
            header.loc[[i],['Home']] = opp[i]
        r = str(result[i]).split(",")
        header.loc[[i],['Result']] = r[0]
        header.loc[[i],['Score']] = r[1]
    data = pd.concat([header, data], axis=1)

    # Sanitize Opp DataFrame
    debris = data_opp[ data_opp['Opp'] != team ].index
    if len(debris) > 0:
        data_opp.drop(debris, inplace=True)
        data_opp = data_opp.reset_index(drop=True)
    date = data_opp['Date']
    home = data_opp['Home']
    opp = data_opp['Opp']
    result = data_opp['Rslt']
    data_opp.drop(['Game','Date','Home','Opp','Rslt','PitchersUsed'], axis=1, inplace=True)
    data_opp = data_opp.reset_index(drop=True)
    header = pd.DataFrame(index=range(0,len(home)), columns = ['Date', 'Visitor','Home','Result','Score'])
    for i in range(len(home)):
        header.loc[[i],['Date']] = date[i]
        if home[i] == True:
            header.loc[[i],['Visitor']] = opp[i]
            header.loc[[i],['Home']] = against
        else:
            header.loc[[i],['Visitor']] = against
            header.loc[[i],['Home']] = opp[i]
        r = str(result[i]).split(",")
        header.loc[[i],['Result']] = r[0]
        header.loc[[i],['Score']] = r[1]
    data_opp = pd.concat([header, data_opp], axis=1)
    
    data = pd.concat([data, data_opp], axis=1)
    data = data.sort_index(ascending=True)
    
    # Sanitize Final Dataframes
    
    
    return data

def get_fgr_split(team, type=['P','B'], opp=None, hand=[None,'L','R'], opphand=[None,'L','R'], time=[None,'D','N'], home=[None,'H','A'], start_date='2017-03-01', end_date='2021-11-01'):
    
    path = chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument('user-agent='+USER_AGENT)
    options.add_argument('headless')
    options.add_argument('start-maximized')
    options.add_argument('disable-gpu')
    driver = webdriver.Chrome(path, options=options)

    # FGR splitArr
    # Batting split
    #     1 = vLHP
    #     2 = vRHP
    #     3 = as LHH
    #     4 = as RHH
    #     7 = Home
    #     8 = Away
    #     90 = Day
    #     91 = Night
    # Pitching split
    #     96 = as RHP
    #     97 = as LHP
    #     5 = v LHH
    #     6 = v RHH   
    #     90 = Day
    #     91 = Night
    #     42 = as SP
    #     43 = as RP
    #     9 = Home
    #     10 = Away
    
    arr = []
    con1="";con2="";con3="";con4=""
    if type == 'P':
        arr.append( str(DICT_FGR_SPLIT[team][2]) )
        if opp:
            arr.append( str(DICT_FGR_SPLIT[opp][3]))
        if hand:
            if hand == 'L':
                con1 = 'L'
                arr.append('96')
            elif hand == 'R':
                con1 = 'R'
                arr.append('97')
        if opphand:
            if opphand == 'L':
                con2 = 'L'
                arr.append('5')
            elif opphand == 'R':
                con2 = 'R'
                arr.append('6')
        if time:
            if time == 'D':
                con3 = 'D'
                arr.append('90')
            elif time =='N':
                con3 = 'N'
                arr.append('91')
        if home:
            if home == 'H':
                con4 = 'H'
                arr.append('9')
            elif home == 'A':
                con4 = 'A'
                arr.append('10')    
    else: #Batting Split
        arr.append(str(DICT_FGR_SPLIT[team][0]))
        if opp:
            arr.append(str(DICT_FGR_SPLIT[opp][1]))
        if hand:
            if hand == 'L':
                con1 = 'L'
                arr.append('3')
            elif hand == 'R':
                con1 = 'R'
                arr.append('4')
        if opphand:
            if opphand == 'L':
                con2 = 'L'
                arr.append('1')
            elif opphand == 'R':
                con2 = 'R'
                arr.append('2')
        if time:
            if time == 'D':
                con3 = 'D'
                arr.append('90')
            elif time =='N':
                con3 = 'N'
                arr.append('91')
        if home:
            if home == 'H':
                con4 = 'H'
                arr.append('7')
            elif home == 'A':
                con4 = 'A'
                arr.append('8')         
    
    splitArr = ",".join(arr)
    URL = URL_FGR['SPLIT'].format(splitArr, type, start_date, end_date)
    print(URL)
    driver.get(URL)
    driver.implicitly_wait(5)
    html = driver.page_source
    driver.close()
    df = pd.read_html(html, encoding='utf-8')
    # df = pd.read_html(html, encoding='utf-8', match=r'^(Season|#)$')
    df = df[-1:][0]
    
    # Sanitize
    try:
        df = df.drop(['#', 'Season', 'Tm'],axis=1)
    except:
        pass
    
    con_arr = []
    for i in range(0, len(df)):
        li = []
        li.append(team)
        li.append(opp)
        li.append(con1)
        li.append(con2)
        li.append(con3)
        li.append(con4)
        con_arr.append(li)
    con_df = pd.DataFrame(data=con_arr, columns=['Team','Opp','H','vH','DN','HA'])
    df = pd.concat([con_df, df], axis=1)

    return df