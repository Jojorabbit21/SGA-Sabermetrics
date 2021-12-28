import pandas as pd
import math
import os.path
from tqdm import tqdm

def push_ump_names(season):
  
  filepath_header = './bakery/umpire_strikezones/'
  exist_filepath = './bakery/umpire_strikezones/refined/refined_{}.csv'.format(season)
  if os.path.isfile(exist_filepath):
    print("File Already Exists. Open Legacy")
    sc_df = pd.read_csv(exist_filepath)
  else:
    print("No File Exists. Create New One.")
    sc_df = pd.read_csv(filepath_header + 'statcast_{}.csv'.format(season))
  
  retrosheet = '{}.csv'.format(season)
  rs_df = pd.read_csv(filepath_header + retrosheet)
  rs_df = rs_df.loc[:,['Date','Visitor','Home','UmpName']]

  for i in tqdm(range(len(sc_df)), desc="Sanitizing {}".format(season)):
    if pd.isnull(sc_df.loc[i,'umpire']):
      try:
        date = int(sc_df.at[i,'game_date'])
        visitor = sc_df.at[i,'away_team']
        home = sc_df.at[i,'home_team']
        index = rs_df[(rs_df['Date'] == date) & (rs_df['Visitor'] == visitor) & (rs_df['Home'] == home)].index
        sc_df.loc[i,'umpire'] = rs_df.at[index[0],'UmpName']
      except:
        pass
  print("Saving Files to refined folder.")
  sc_df.to_csv('./bakery/umpire_strikezones/refined/refined_{}.csv'.format(season))
  
if __name__ == '__main__':
  for season in range(2015,2022):
    push_ump_names(season)