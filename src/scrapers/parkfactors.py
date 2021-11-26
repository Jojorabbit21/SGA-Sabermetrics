import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.utils.constants import *
from src.utils.dictionaries import *

def get_park_factors():
  park_factors = pd.read_html(URL_LINEUPS['PARK_FACTORS'],encoding='utf-8')
  park_factors = park_factors[0].drop(['Game', 'Time (GMT)'], axis=1)
  return park_factors
