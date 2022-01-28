import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os.path
import math
from tqdm import tqdm

'''
Umpire Stats
1. Called strike inside the zone
-> zone distance 를 통해 call accuracy 산출
-> hawkeye stats 만들어보기
2. Called strike but out of zone
-> zone distance 를 통해 call accuracy 산출
3. Called ball but inside the zone
-> zone distance 를 통해 call accuracy 산출
'''

# Ump List 추출
def get_ump_list():
  filepath = './rawfish/umpires/ump_scorecards/umpires.csv'
  df = pd.read_csv(filepath)
  return df

# Ump 이름별로 csv 파일 생성
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

# Ump 이름별로 기록 저장
def push_ump_history(full, abbr):
  if os.path.isfile("./bakery/umpire_strikezones/refined/umpires/{}.csv".format(abbr)):
    print("Pushing {}'s Umpire Records".format(full))
    for season in range(2015,2022):
      df = pd.read_csv('./bakery/umpire_strikezones/refined/refined_{}.csv'.format(season))
      df = df[df['umpire'] == full]
      df.to_csv("./bakery/umpire_strikezones/refined/umpires/{}.csv".format(abbr), mode='a', encoding='utf-8-sig', header=False, index=False)
  else:
    print("there is no umpire {}.".format(full))


# statcast 파일의 비어있는 umpire column 채우기
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
  



# 시각화
def vizualize_umpire(full, abbr):
  if os.path.isfile("./bakery/umpire_strikezones/refined/umpires/{}.csv".format(abbr)):
    print("Visualizing {}'s pitch-by-pitch record".format(full))
    history = pd.read_csv("./bakery/umpire_strikezones/refined/umpires/{}.csv".format(abbr))

    # Data Visualization 
    # Total Zone = (-2 <= x <= 2) & (1 <= z <= 4.5)
    # Strike =  (-1 <= plate_x <= 1) && (1.5 <= plate_z <= 3.5) 
    # Borderline = ((-1.2 <= plate_x <= -0.8) || (0.8 <= plate_x <= 1.2)) && ((1.3 <= plate_z <= 1.7) || (3.3 <= plate_z <= 3.7))
    history = history.query('call == "r" or call == "w"')
    palette = {
      'S': 'orange',
      'B': 'limegreen'
    }
    markers = {
      'r': 'o',
      'w': 'X'
    }
    fig , sax = plt.subplots(1,1, figsize=(20,20))
    sax = sns.scatterplot(x=history['plate_x'], y=history['plate_z'], s=20 ,style=history['call'] , hue=history['type'], palette=palette, markers=markers)
    sax.set_xlim(-2,2)
    sax.set_ylim(1,4)
    sax.set_title('{} - InsideSZ Scatter plot'.format(full))
    sax.set_xlabel('vLHP')
    sax.set_ylabel('')
    sax.add_patch(patches.Rectangle((-1,1.5),2,2, edgecolor='black', fill=False, alpha=0.4))
    plt.grid(True, color='gray', alpha=0.3, linestyle='--')
    dest_path = './bakery/umpire_strikezones/refined/umpires/images/{}.png'.format(abbr)
    if not os.path.isfile(dest_path):
      plt.savefig(dest_path, facecolor='#eeeeee', dpi=300)
    plt.close()


# borderline call 정확도 구하기
def evaluate_proximity(abbr):
  # Borderline = ((-1.2 <= plate_x <= -1) || (1 <= plate_x <= 1.2)) && ((1.3 <= plate_z <= 1.5) || (3.5 <= plate_z <= 3.7))
  # 정확히 보더라인인 객체와 얼마나 가까운지? target_distance/border_distance => -0.8/-1 => 0.8/1 => 80%
  exist_filepath = './bakery/umpire_strikezones/refined/umpires/{}.csv'.format(abbr)
  if os.path.isfile(exist_filepath):
    df = pd.read_csv(exist_filepath)
    df_length = len(df)
    print("Evaluate {}'s Call Proximity".format(abbr))
        
    y = 0
    n = 0
    allowed = ['called_strike','ball','blocked_ball']
    
    for i in tqdm(range(df_length)):
      if math.isnan(df.loc[i,'plate_x']) and math.isnan(df.loc[i,'plate_z']):
        n += 1
        continue
      else:
        des = df.at[i, 'description']
        plate_x = df.loc[i,'plate_x']
        plate_z = df.loc[i,'plate_z']
        type = df.loc[i,'type']
        if des in allowed:
          if type == 'S':
            if des == 'called_strike': # If called Strike
              if (-1 <= plate_x <= 1):
                if (1.5 <= plate_z <= 3.5):
                  call = 'r'
                else:
                  call = 'w'
              else:
                call = 'w'
              df.loc[i,'call'] = call
              y += 1
          elif type == 'B':
            if des == 'ball' or des == 'blocked_ball': # If Called Ball (Intent Ball is not included)
              if (plate_x < -1 or plate_x > 1) or (plate_z < 1.5 or plate_z > 3.5):
                call = 'r'
              elif (-1 <= plate_x <= 1) and (1.5 <= plate_z <= 3.5):
                call = 'w'
              df.loc[i,'call'] = call
              y += 1
          else:
            continue
        else:
          continue
    print(f"{abbr} Evaluated: Filled: {y} / Void: {n}")
    df.to_csv(exist_filepath,mode="w",encoding='utf-8-sig',index=False)
    
def get_ump_ranks(abbr):
  exist_filepath = './bakery/umpire_strikezones/refined/umpires/{}.csv'.format(abbr)
  if os.path.isfile(exist_filepath):  
    df = pd.read_csv(exist_filepath)
    print("Evaluate {}'s Rank".format(abbr))
    total = df.loc[(df['type'] == 'B')|(df['type'] == 'S'),['pitch_type','type','call']]
    pitchtype_acc = total.groupby(['pitch_type','call']).count()
    ball_total = df.loc[(df['type'] == 'B')&(df['call'] == 'r')|(df['call'] == 'w'),['type','call']]
    ball_acc = ball_total.groupby(['call']).count()
    strike_total = df.loc[(df['type'] == 'S')&(df['call'] == 'r')|(df['call'] == 'w'),['type','call']]
    strike_acc = strike_total.groupby(['call']).count()
    # print(f"Total: {len(strike_total)+len(ball_total)}")
    # print(ball_acc)
    # print(strike_acc)
    print(pitchtype_acc)

if __name__ == '__main__':

  # --- Testing ---
  # evaluate_proximity('angel_hernandez')
  get_ump_ranks('adam_beck')
  # vizualize_umpire('Angel Hernandez','angel_hernandez')
  
  # df = get_ump_list()
  # create_ump_history(df['Abbr'])
  # for i in range(len(df)):
    # abbr = df.at[i,'Abbr']
    # push_ump_history(str(df.at[i,'Umpire']),str(df.at[i,'Abbr']))
    # evaluate_proximity(abbr)
    # get_ump_ranks(abbr)
    # vizualize_umpire(df.at[i,'Umpire'], abbr)
