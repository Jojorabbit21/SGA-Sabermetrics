import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

from src.utils.constants import *
from src.utils.dictionaries import *

gameinfo_df_col = [
  # Game info
  'Match',
  'Game ID',
  'Visitor',
  'Home',
  'Time',
  'Wind Direction',
  'Wind Speed',
  'Tempurature',
  'Humidity',
  # Pitcher info
  'Pitcher',
  'Pitcher ID',
  'Pitcher Hand',
  # Batter info
  'Batter 1',
  'Batter 1 ID',
  'Batter 1 Pos',
  'Batter 1 Hand',
  'Batter 2',
  'Batter 2 ID',
  'Batter 2 Pos',
  'Batter 2 Hand',
  'Batter 3',
  'Batter 3 ID',
  'Batter 3 Pos',
  'Batter 3 Hand',
  'Batter 4',
  'Batter 4 ID',
  'Batter 4 Pos',
  'Batter 4 Hand',
  'Batter 5',
  'Batter 5 ID',
  'Batter 5 Pos',
  'Batter 5 Hand',
  'Batter 6',
  'Batter 6 ID',
  'Batter 6 Pos',
  'Batter 6 Hand',
  'Batter 7',
  'Batter 7 ID',
  'Batter 7 Pos',
  'Batter 7 Hand',
  'Batter 8',
  'Batter 8 ID',
  'Batter 8 Pos',
  'Batter 8 Hand',
  'Batter 9',
  'Batter 9 ID',
  'Batter 9 Pos',
  'Batter 9 Hand'
]

def sanitize_teamname(name:str):
  if name in DICT_SANITIZE:
    sanitized = DICT_SANITIZE[name]
    return sanitized
  else:
    return name

def get_matches(date):
  headers={'User-Agent':USER_AGENT}
  r = requests.get(URL_RG['LINEUP']+date, headers=headers)
  r.encoding = 'utf-8'
  if r.status_code == 200:
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    
    # Getting Team names, Game schedules
    cards = soup.find_all('li', attrs={'data-role': 'lineup-card'})
    # Sanitizing Team names
    gameid = []; team_names = []; match = []
    for i in range(len(cards)):
      gameid.append(cards[i]['data-schedule-id'])
      visit = sanitize_teamname(cards[i]['data-away'])
      home = sanitize_teamname(cards[i]['data-home'])
      team_names.append(visit)
      team_names.append(home)
      match.append(visit+"@"+home)

    # Getting Game time
    time = soup.find_all('time')
    # Sanitizing Game time
    gametime = []
    for i in time:
      gametime.append(i.text)

    # weather = soup.find_all('div', attrs={'class':'div.blk.weather'})
    weather = soup.select('div.blk.weather')
    wind_direction = []; wind_speed = []; temp = []; humidity = []
    # Sanitizing Game Info
    for i in weather:
      if len(i.text) > 1:
        # Sanitizing WD
        wd = i.select_one('div.wind-status > span')
        wd = re.search(r'[A-Z]+',str(wd['class']))
        wind_direction.append(wd.group())
        # Sanitizing WS
        ws = i.select_one('div.wind-status > ul > li:nth-child(1) > span:nth-child(1) > span').text
        wind_speed.append(ws)
        # Sanitizing TP
        tp = i.select_one('div.wind-status > ul > li:nth-child(1) > span.humidity').text
        temp.append(tp)
        # Sanitizing HD
        hd = i.select_one('div.wind-status > ul > li.humidity').text
        hd = re.sub(' humidity','',hd)
        humidity.append(hd)
      else:
        wind_direction.append('None')
        wind_speed.append('None')
        temp.append('None')
        humidity.append('None')
        
    # Getting All Players
    players = soup.find_all("a",attrs={'class': 'player-popup'})
    # Sanitizing
    all_players = [] # [ rows = match length / cols = 20 ]
    playerids = [] # [ rows = match length / cols = 20 ]
    for i in range(len(match)):
      pls = []
      pis = []
      for j in range(0, 20):
        pls.append(players[(i*20)+j].text)
        pis.append(re.sub(r'[^0-9]','',players[i]['data-url']))
      all_players.append(pls)
      playerids.append(pis)
  
    # Getting Pitchers Hand
    pit_hand = soup.select('div.blk.game > div.blk > div > span > span.stats')
    visitor_pitcher_hand = []; home_pitcher_hand = []
    # Sanitizing
    for i in range(len(match)):
      for j in range(0,2):
        ph = str
        if j == 0:
          ph = str(pit_hand[(i*2)+j].text).replace('\n','').replace(' ','')
          visitor_pitcher_hand.append(ph)
        else:
          ph = str(pit_hand[(i*2)+j].text).replace('\n','').replace(' ','')
          home_pitcher_hand.append(ph)         
    
    # Getting Batters Position / Hand
    pos = soup.find_all("span",attrs={'class': 'position'})
    bat_hand = soup.select("div.blk.game > div.blk > ul > li > div > span.stats > span.status > span.stats")
    batter_hand = []
    batter_position = []
    # Sanitizing
    for i in range(len(match)):
      bp = []; bh = []
      for j in range(0, 18):
        bp.append(str(pos[(i*18)+j].text).replace('\n','').replace(' ',''))
        bh.append(str(bat_hand[(i*18)+j]['data-hand']))
      batter_hand.append(bh)
      batter_position.append(bp)
    
    df = pd.DataFrame(batter_position)
    print(df)
    
    # Merging Player info
    # match_counter = 0; list_counter = 0
    # for i in range(len(match)):
    #   row = []
    #   for j in range(0,20):
    #     if j == 0 or j == 10:
    #       row.append(all_players[i])
          
          
    
    #dataframe 으로 merge
    gameinfo_df = pd.DataFrame()

  return gameinfo_df
      
