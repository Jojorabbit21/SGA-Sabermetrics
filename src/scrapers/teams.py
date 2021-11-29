import pandas as pd
import datetime
from time import sleep, time

from src.utils.constants import *
from src.utils.dictionaries import *

from pybaseball.team_batting import *
from pybaseball import team_fielding
from pybaseball.team_pitching import *
from pybaseball import team_game_logs

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# options = Options()
# user_agent = "Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36"
# options.add_argument('user-agent=' + user_agent)
# # options.add_argument('headless') #headless모드 브라우저가 뜨지 않고 실행됩니다.
# options.add_argument('disable-gpu')
# # options.add_argument('--window-size= x, y') #실행되는 브라우저 크기를 지정할 수 있습니다.
# options.add_argument('--start-maximized') #브라우저가 최대화된 상태로 실행됩니다.
# # options.add_argument('--start-fullscreen') #브라우저가 풀스크린 모드(F11)로 실행됩니다.
# # options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
# # options.add_argument('--mute-audio') #브라우저에 음소거 옵션을 적용합니다.
# # options.add_argument('incognito') #시크릿 모드의 브라우저가 실행됩니다.

from src.utils.dictionaries import DICT_SOURCE, DICT_TEAMNAMES

# 각 팀 선수별 타격 지표
def get_team_batting(team, start_season=2010, end_season=2021):
    data = team_batting_bref(team, start_season, end_season)
    return data

# 각 팀별 타격지표
def get_team_batting_table(start_season=2012, end_season=2021):
    data = team_batting(start_season=start_season, end_season=end_season, league='ALL', ind=1)
    data.sort_values(by=['Team','Season'],axis=0, ascending=[True, True], inplace=True)
    data.reset_index(inplace=True, drop=True)
    return data

# 각 팀 선수별 수비 지표
def get_team_fielding(team, start_season=2015, end_season=2021):
    data = team_fielding.team_fielding_bref(team, start_season=start_season, end_season=end_season)
    return data

# 각 팀별 수비지표 => DSR, UZR 등 추출
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
    return data

# 각 팀 선수별 투수지표
def get_team_pitching(team, start_season=2010, end_season=2021):
    data = team_pitching_bref(team, start_season=start_season, end_season=end_season)
    return data

# 각 팀별 투수지표 -> 318컬럼 ; 에반데
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
    return data

# 상대전적 검색
def get_head_to_head(team, against, year:int=2021, log_type="batting"):
    team = DICT_TEAMNAMES[team][DICT_SOURCE['BBREFTEAM']]
    against = DICT_TEAMNAMES[against][DICT_SOURCE['BBREFTEAM']]
    data = team_game_logs(season=year, team=team, log_type=log_type)
    
    # Sanitize DataFrame
    debris = data[ data['Opp'] != against ].index
    if len(debris) > 0:
        data.drop(debris, inplace=True)
        data = data.reset_index(drop=True)
    date = data['Date']
    home = data['Home']
    opp = data['Opp']
    result = data['Rslt']
    data.drop(['Game','Date','Home','Opp','Rslt'], axis=1, inplace=True)
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
    
    return data

def get_fgr_split(team, type=['P','B'], opp=None, hand=[None,'L','R'], opphand=[None,'L','R'], time=[None,'D','N'], home=[None,'H','A'], start_date='2021-03-01', end_date='2021-11-01'):
    
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
    if type == 'P':
        arr.append( str(DICT_FGR_SPLIT[team][0]) )
        if opp:
            arr.append( str(DICT_FGR_SPLIT[team][1]))
        if hand:
            if hand == 'L':
                arr.append('3')
            elif hand == 'R':
                arr.append('4')
        if opphand:
            if opphand == 'L':
                arr.append('1')
            elif opphand == 'R':
                arr.append('2')
        if time:
            if time == 'D':
                arr.append('90')
            elif time =='N':
                arr.append('91')
        if home:
            if home == 'H':
                arr.append('7')
            elif home == 'A':
                arr.append('8')    
    else:
        arr.append(str(DICT_FGR_SPLIT[team][2]))
        if opp:
            arr.append(str(DICT_FGR_SPLIT[team][3]))
        if hand:
            if hand == 'L':
                arr.append('96')
            elif hand == 'R':
                arr.append('97')
        if opphand:
            if opphand == 'L':
                arr.append('5')
            elif opphand == 'R':
                arr.append('6')
        if time:
            if time == 'D':
                arr.append('90')
            elif time =='N':
                arr.append('91')
        if home:
            if home == 'H':
                arr.append('9')
            elif home == 'A':
                arr.append('10')         
    
    splitArr = ",".join(arr)
    URL = URL_FGR['SPLIT'].format(splitArr, type, start_date, end_date)
    print(URL)
    # fangraphs말고 bbref로 진행
    # driver = webdriver.Chrome(executable_path='./src/scrapers/chromedriver.exe', options=options)
    # driver.get(URL)
    # sleep(5)
    # html = driver.page_source
    # driver.close()
    # df = pd.read_html(html)
    # print(len(df))
    # print(df)
    
    # return df