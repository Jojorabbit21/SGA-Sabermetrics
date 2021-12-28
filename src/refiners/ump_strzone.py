import pandas as pd
import math
from tqdm import tqdm

def push_ump_names(season):
  
  filepath = './bakery/umpire_strikezones/'
  retrosheet = '{}.csv'.format(season)
  statcast = 'statcast_{}.csv'.format(season)
  
  rs_df = pd.read_csv(filepath + retrosheet)
  sc_df = pd.read_csv(filepath + statcast)
  
  rs_df = rs_df.loc[:,['Date','Visitor','Home','UmpName']]
  
  for i in tqdm(range(len(sc_df)), desc="Sanitizing {}".format(season)):
    if math.isnan(sc_df.loc[i,'umpire']):
      try:
        date = int(sc_df.at[i,'game_date'])
        visitor = sc_df.at[i,'away_team']
        home = sc_df.at[i,'home_team']
        index = rs_df[(rs_df['Date'] == date) & (rs_df['Visitor'] == visitor) & (rs_df['Home'] == home)].index
        sc_df.loc[i,'umpire'] = rs_df.at[index[0],'UmpName']
      except:
        pass

  sc_df.to_csv('./bakery/umpire_strikezones/refined/refined_{}.csv'.format(season))
  
if __name__ == '__main__':
  push_ump_names(2021)