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
  # Player info
  'Visitor Pitcher',
  'Visitor Batter 1',
  'Visitor Batter 2',
  'Visitor Batter 3',
  'Visitor Batter 4',
  'Visitor Batter 5',
  'Visitor Batter 6',
  'Visitor Batter 7',
  'Visitor Batter 8',
  'Visitor Batter 9',
  'Home Pitcher',
  'Home Batter 1',
  'Home Batter 2',
  'Home Batter 3',
  'Home Batter 4',
  'Home Batter 5',
  'Home Batter 6',
  'Home Batter 7',
  'Home Batter 8',
  'Home Batter 9',
  'Visitor Pitcher ID',
  'Visitor Batter 1 ID',
  'Visitor Batter 2 ID',
  'Visitor Batter 3 ID',
  'Visitor Batter 4 ID',
  'Visitor Batter 5 ID',
  'Visitor Batter 6 ID',
  'Visitor Batter 7 ID',
  'Visitor Batter 8 ID',
  'Visitor Batter 9 ID',
  'Home Pitcher ID',
  'Home Batter 1 ID',
  'Home Batter 2 ID',
  'Home Batter 3 ID',
  'Home Batter 4 ID',
  'Home Batter 5 ID',
  'Home Batter 6 ID',
  'Home Batter 7 ID',
  'Home Batter 8 ID',
  'Home Batter 9 ID',
  'Visitor Pitcher Hand',
  'Home Pitcher Hand',
  'Visitor Batter 1 Hand',
  'Visitor Batter 2 Hand',
  'Visitor Batter 3 Hand',
  'Visitor Batter 4 Hand',
  'Visitor Batter 5 Hand',
  'Visitor Batter 6 Hand',
  'Visitor Batter 7 Hand',
  'Visitor Batter 8 Hand',
  'Visitor Batter 9 Hand',
  'Home Batter 1 Hand',
  'Home Batter 2 Hand',
  'Home Batter 3 Hand',
  'Home Batter 4 Hand',
  'Home Batter 5 Hand',
  'Home Batter 6 Hand',
  'Home Batter 7 Hand',
  'Home Batter 8 Hand',
  'Home Batter 9 Hand',
  'Visitor Batter 1 Pos',
  'Visitor Batter 2 Pos',
  'Visitor Batter 3 Pos',
  'Visitor Batter 4 Pos',
  'Visitor Batter 5 Pos',
  'Visitor Batter 6 Pos',
  'Visitor Batter 7 Pos',
  'Visitor Batter 8 Pos',
  'Visitor Batter 9 Pos',
  'Home Batter 1 Pos',
  'Home Batter 2 Pos',
  'Home Batter 3 Pos',
  'Home Batter 4 Pos',
  'Home Batter 5 Pos',
  'Home Batter 6 Pos',
  'Home Batter 7 Pos',
  'Home Batter 8 Pos',
  'Home Batter 9 Pos',
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
    gameid = []; team_names_visit = []; team_names_home = []; match = []
    for i in range(len(cards)):
      gameid.append(cards[i]['data-schedule-id'])
      visit = sanitize_teamname(cards[i]['data-away'])
      home = sanitize_teamname(cards[i]['data-home'])
      team_names_visit.append(visit)
      team_names_home.append(home)
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
    
    game_df = pd.DataFrame()
    game_df['A'] = match
    game_df['B'] = gameid
    game_df['C'] = team_names_visit
    game_df['D'] = team_names_home
    game_df['E'] = gametime
    game_df['F'] = wind_direction
    game_df['G'] = wind_speed
    game_df['H'] = temp
    game_df['I'] = humidity
    
        
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
        pis.append(re.sub(r'[^0-9]','',players[(i*20)+j]['data-url']))
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
    
    player_df = pd.DataFrame(all_players)
    playerid_df = pd.DataFrame(playerids)
    vph_df = pd.DataFrame(visitor_pitcher_hand)
    hph_df = pd.DataFrame(home_pitcher_hand)
    bh_df = pd.DataFrame(batter_hand)
    bp_df = pd.DataFrame(batter_position)
    
    players_df = pd.concat([player_df, playerid_df, vph_df, hph_df, bh_df, bp_df], axis=1)

    game_df = pd.concat([game_df, players_df], axis=1)
    game_df.columns = gameinfo_df_col

  return game_df, players_df
      
