import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.utils.constants import *
from src.utils.dictionaries import *

def get_matches(date):
  headers={'User-Agent':USER_AGENT}
  r = requests.get(URL_RG['LINEUP']+date, headers=headers)
  r.encoding = 'utf-8'
  if r.status_code == 200:
    html = r.text
    soup = BeautifulSoup(html, 'lxml')

    visitors = soup.find_all("span",attrs={'class':'shrt'})
    players = soup.find_all("a",attrs={'class': 'player-popup'})
    pit_hand = soup.select('div.blk.game > div.blk > div > span > span.stats')
    position = soup.find_all("span",attrs={'class': 'position'})
    bat_hand = soup.select("div.blk.game > div.blk > ul > li > div > span.stats > span.status > span.stats")
    for i in bat_hand:
      h = i['data-hand']
      
    time = soup.find_all('div',attrs={'class':'weather-status'})
    weather = soup.select('div.wind-status > ul > li:nth-child(1) > span:nth-child(1)')
    for i in weather:
          print(i.text)
    # 날씨랑 습도 가져오는게 문제네 있는것도 있고 없는것도 있고... game length 구해서 for 문으로 selector 에 숫자 넣어서 값을 가져오고 없는 것은 NaN 등록?     
      
    #pit_hand , position , time , weather sanitize
    #dataframe 으로 merge

  return 0, 0
      
