import pandas as pd
from pybaseball import statcast
from multiprocessing import Process, freeze_support

'''
https://umpscorecards.com/site-data/umpires.html
https://umpscorecards.com/site-data/teams.html
https://umpscorecards.com/site-data/games.html

'''

def get_statcast_logs(filepath, start_season:int, end_season:int):
  freeze_support()  
  for season in range(start_season,end_season):
    data = statcast(str(season)+'-01-01',str(season)+'-12-01')
    data.to_csv(filepath+'statcast_'+str(season)+ '.csv')
    
