import pandas as pd
import math
import os.path
from tqdm import tqdm

def get_ump_list():
  filepath = './rawfish/umpires/ump_scorecards/umpires.csv'
  df = pd.read_csv(filepath)
  return df

def create_ump_history(namelist):
  created = 0
  columns = ['pitch_type','game_date','release_speed','release_pos_x','release_pos_z','spin_axis','batter','pitcher',
             'events','description','zone','stand','p_throws','home_team','away_team','type','hit_location','bb_type','plate_x','plate_z','umpire','delta_run_exp']
  for name in namelist:
    filepath = './bakery/umpire_strikezones/refined/umpires/{}.csv'.format(name)
    if not os.path.isfile(filepath):
      df = pd.DataFrame(columns=columns)
      df.to_csv(filepath)
      created += 1
    else:
      continue
  print("{} file created".format(created))
  
def push_ump_history(full, abbr):
  if os.path.isfile("./bakery/umpire_strikezones/refined/umpires/{}.csv".format(abbr)):
    print("Pushing {}'s Umpire Records".format(full))
    for season in range(2015,2022):
      df = pd.read_csv('./bakery/umpire_strikezones/refined/refined_{}.csv'.format(season))
      df = df[df['umpire'] == full]
      df.to_csv("./bakery/umpire_strikezones/refined/umpires/{}.csv".format(abbr), mode='a', encoding='utf-8-sig', header=False)
  else:
    print("there is no umpire {}.".format(full))

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
  
  res_df = pd.DataFrame()
  
  for i in tqdm(range(len(rs_df)), desc='Sanitizing {}'.format(season)):
    target_date = int(rs_df.at[i, 'Date'])
    target_visitor = str(rs_df.at[i, 'Visitor'])
    target_home = str(rs_df.at[i, 'Home'])
    target_umpname = str(rs_df.at[i, 'UmpName'])  
    df = sc_df[(sc_df['game_date'] == target_date) & (sc_df['away_team'] == target_visitor) & (sc_df['home_team'] == target_home)]
    df = df.loc[:,['pitch_type','game_date','release_speed','release_pos_x','release_pos_z','spin_axis','batter','pitcher','events','description','zone','stand','p_throws',
                  'home_team','away_team','type','hit_location','bb_type','plate_x','plate_z','umpire','delta_run_exp']]
    df[['umpire']] = df[['umpire']].fillna(target_umpname)
    res_df = pd.concat([res_df, df], axis=0)
    
  print("Saving Files to refined folder.")  
  res_df.to_csv('./bakery/umpire_strikezones/refined/refined_{}.csv'.format(season))    
  
if __name__ == '__main__':
  df = get_ump_list()
  create_ump_history(df['Abbr'])
  for i in range(len(df)):
    push_ump_history(str(df.at[i,'Umpire']),str(df.at[i,'Abbr']))