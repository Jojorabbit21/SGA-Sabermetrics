from os import cpu_count
import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.utils.constants import *
from src.utils.dictionaries import *

def get_park_factors():
  park_factors = pd.read_html(URL_LINEUPS['PARK_FACTORS'],encoding='utf-8')
  park_factors = park_factors[0].drop(['Game', 'Time (GMT)'], axis=1)
  team = []
  for i in range(0,len(park_factors)):
    name = park_factors.loc[[i],['Park']].to_numpy()
    name = str(name[0][0]).replace(' ( ', ',')
    name = name.replace(' )', '')
    name = name.split(',')
    park_factors.loc[[i],['Park']] = name[0]
    team.append(name[1])
  teams = pd.DataFrame(team, columns=['Team'])
  park_factors = pd.concat([teams, park_factors], axis = 1)
  return park_factors
