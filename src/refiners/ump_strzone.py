import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os.path
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
      df.to_csv("./bakery/umpire_strikezones/refined/umpires/{}.csv".format(abbr), mode='a', encoding='utf-8-sig', header=False, index=False)
  else:
    print("there is no umpire {}.".format(full))

def sanitize_ump_history(full, abbr):
  if os.path.isfile("./bakery/umpire_strikezones/refined/umpires/{}.csv".format(abbr)):
    print("Sanitizing {}'s pitch-by-pitch record".format(full))
    history = pd.read_csv("./bakery/umpire_strikezones/refined/umpires/{}.csv".format(abbr))

    # Data Visualization 
    # Total Zone = (-2 <= x <= 2) & (1 <= z <= 4.5)
    # Strike =  (-1 <= plate_x <= 1) && (1.5 <= plate_z <= 3.5) 
    # Borderline = ((-1.2 <= plate_x <= -0.8) || (0.8 <= plate_x <= 1.2)) && ((1.3 <= plate_z <= 1.7) || (3.3 <= plate_z <= 3.7))
    
    # 1. Called Strike but Out of SZ
    #    1-1. vLHP
    #    1-2. vRHP
    # 2. Called Strike Inside SZ
    #    2-1. vLHP
    #    2-2. vRHP
    # 3. Called Ball but Inside SZ
    #    3-1. vLHP
    #    3-2. vRHP
    
    # # called strike but out of strikezone
    # ooz = history.query('(plate_x < -1 or plate_x > 1) or (plate_z < 1.5 or plate_z > 3.5) and (type == "S" or type == "X") and description == "called_strike"')
    # ooz_lhp = ooz.query('p_throws == "L"')
    # ooz_lhp_x = ooz_lhp['plate_x']
    # ooz_lhp_y = ooz_lhp['plate_z']
    # ooz_rhp = ooz.query('p_throws == "R"')
    # ooz_rhp_x = ooz_rhp['plate_x']
    # ooz_rhp_y = ooz_rhp['plate_z']
    
    # fig, ax = plt.subplots(1,1, figsize=(10,8))
    # ax = sns.kdeplot(x=ooz_lhp_x, y=ooz_lhp_y, cmap="OrRd", shade=True)
    # ax.set_xlim(-2, 2)
    # ax.set_ylim(1, 4)
    # ax.set_title('{} - Strike/OutofSZ'.format(full))
    # ax.set_xlabel('vLHP')
    # ax.set_ylabel('')
    # ax.add_patch(patches.Rectangle((-1,1.5),2,2, edgecolor='black', fill=False))
    # plt.grid(True, color='gray', alpha=0.4, linestyle='--')
    # dest_path = './bakery/umpire_strikezones/refined/umpires/images/{}_ooz_lhp.png'.format(abbr)
    # if not os.path.isfile(dest_path):
    #   plt.savefig(dest_path, facecolor='#eeeeee')
    
    # fig, ax = plt.subplots(1,1, figsize=(10,8))
    # ax = sns.kdeplot(x=ooz_rhp_x, y=ooz_rhp_y, cmap="OrRd", shade=True)
    # ax.set_xlim(-2, 2)
    # ax.set_ylim(1, 4)
    # ax.set_title('{} - Strike/OutofSZ'.format(full))
    # ax.set_xlabel('vRHP')
    # ax.set_ylabel('')
    # ax.add_patch(patches.Rectangle((-1,1.5),2,2, edgecolor='black', fill=False))
    # plt.grid(True, color='gray', alpha=0.4, linestyle='--')
    # dest_path = './bakery/umpire_strikezones/refined/umpires/images/{}_ooz_rhp.png'.format(abbr)
    # if not os.path.isfile(dest_path):
    #   plt.savefig(dest_path, facecolor='#eeeeee')
    # # called strike inside strikezone (vLHP,rRHP)
    # iz = history.query('(plate_x > -1 and plate_x < 1) and (plate_z > 1.5 and plate_z < 3.5) and (type == "S" or type == "X") and description == "called_strike"')
    # iz_lhp = iz.query('p_throws == "L"')
    # iz_lhp_x = iz_lhp['plate_x']
    # iz_lhp_y = iz_lhp['plate_z']
    # iz_rhp = iz.query('p_throws == "R"')
    # iz_rhp_x = iz_rhp['plate_x']
    # iz_rhp_y = iz_rhp['plate_z']
    
    # fig, ax = plt.subplots(1,1, figsize=(10,8))
    # ax = sns.kdeplot(x=iz_lhp_x, y=iz_lhp_y, cmap="OrRd", shade=True)
    # ax.set_xlim(-2, 2)
    # ax.set_ylim(1, 4)
    # ax.set_title('{} - Strike/InsideSZ'.format(full))
    # ax.set_xlabel('vLHP')
    # ax.set_ylabel('')
    # ax.add_patch(patches.Rectangle((-1,1.5),2,2, edgecolor='black', fill=False))
    # plt.grid(True, color='gray', alpha=0.4, linestyle='--')
    # dest_path = './bakery/umpire_strikezones/refined/umpires/images/{}_iz_lhp.png'.format(abbr)
    # if not os.path.isfile(dest_path):
    #   plt.savefig(dest_path, facecolor='#eeeeee') 
    
    # fig, ax = plt.subplots(1,1, figsize=(10,8))
    # ax = sns.kdeplot(x=iz_rhp_x, y=iz_rhp_y, cmap="OrRd", shade=True)
    # ax.set_xlim(-2, 2)
    # ax.set_ylim(1, 4)
    # ax.set_title('{} - Strike/InsideSZ'.format(full))
    # ax.set_xlabel('vRHP')
    # ax.set_ylabel('')
    # ax.add_patch(patches.Rectangle((-1,1.5),2,2, edgecolor='black', fill=False))
    # plt.grid(True, color='gray', alpha=0.4, linestyle='--')
    # dest_path = './bakery/umpire_strikezones/refined/umpires/images/{}_iz_rhp.png'.format(abbr)
    # if not os.path.isfile(dest_path):
    #   plt.savefig(dest_path, facecolor='#eeeeee')  

    # called ball but inside strikezone (vLHP,vRHP)
    biz = history.query('(plate_x > -1 and plate_x < 1) and (plate_z > 1.5 and plate_z < 3.5) and type == "B"')
    biz_lhp = biz.query('p_throws == "L"')
    biz_lhp_x = biz_lhp['plate_x']
    biz_lhp_y = biz_lhp['plate_z']
    biz_rhp = biz.query('p_throws == "R"')
    biz_rhp_x = biz_rhp['plate_x']
    biz_rhp_y = biz_rhp['plate_z']
    
    fig , sax = plt.subplots(1,1)
    sax = sns.scatterplot(x=biz_lhp_x, y=biz_lhp_y, s=500, facecolor='w', edgecolor='r', linewidth=2, alpha=0.3)
    sax.set_xlim(-2,2)
    sax.set_ylim(1,4)
    sax.set_title('{} - Ball/InsideSZ Scatter plot'.format(full))
    sax.set_xlabel('vLHP')
    sax.set_ylabel('')
    sax.add_patch(patches.Rectangle((-1,1.5),2,2, edgecolor='black', fill=False, alpha=0.4))
    plt.grid(True, color='gray', alpha=0.3, linestyle='--')
    plt.show()
    
    # fig, ax = plt.subplots(1,1, figsize=(10,8))
    # ax = sns.kdeplot(x=biz_lhp_x, y=biz_lhp_y, cmap="OrRd", shade=True)
    # ax.set_xlim(-2, 2)
    # ax.set_ylim(1, 4)
    # ax.set_title('{} - Ball/InsideSZ'.format(full))
    # ax.set_xlabel('vLHP')
    # ax.set_ylabel('')
    # ax.add_patch(patches.Rectangle((-1,1.5),2,2, edgecolor='black', fill=False))
    # plt.grid(True, color='gray', alpha=0.4, linestyle='--')
    # dest_path = './bakery/umpire_strikezones/refined/umpires/images/{}_biz_lhp.png'.format(abbr)
    # if not os.path.isfile(dest_path):
    #   plt.savefig(dest_path, facecolor='#eeeeee') 
    
    # fig, ax = plt.subplots(1,1, figsize=(10,8))
    # ax = sns.kdeplot(x=biz_rhp_x, y=biz_rhp_y, cmap="OrRd", shade=True)
    # ax.set_xlim(-2, 2)
    # ax.set_ylim(1, 4)
    # ax.set_title('{} - Ball/InsideSZ'.format(full))
    # ax.set_xlabel('vRHP')
    # ax.set_ylabel('')
    # ax.add_patch(patches.Rectangle((-1,1.5),2,2, edgecolor='black', fill=False))
    # plt.grid(True, color='gray', alpha=0.4, linestyle='--')
    # dest_path = './bakery/umpire_strikezones/refined/umpires/images/{}_biz_rhp.png'.format(abbr)
    # if not os.path.isfile(dest_path):
    #   plt.savefig(dest_path, facecolor='#eeeeee')     

def evaluate_proximity(season):
  # Borderline = ((-1.2 <= plate_x <= -1) || (1 <= plate_x <= 1.2)) && ((1.3 <= plate_z <= 1.5) || (3.5 <= plate_z <= 3.7))
  # 정확히 보더라인인 객체와 얼마나 가까운지? target_distance/border_distance => -0.8/-1 => 0.8/1 => 80%
  exist_filepath = './bakery/umpire_strikezones/refined/refined_{}.csv'.format(season)
  if os.path.isfile(exist_filepath):
    df = pd.read_csv(exist_filepath)
    df_length = len(df)
    print("Evaluate {} Proximity".format(season))
    prox = pd.DataFrame(index=range(df_length), columns=['prox_x','prox_z','prox_pos_x','prox_pos_z'])
    for i in range(df_length):
      plate_x = df.at[i, 'plate_x']
      plate_z = df.at[i, 'plate_z']
      if plate_x < -1: # left of border_x
        prox.loc[i, 'prox_pos_x'] = 'out'
      elif plate_x > 1: # right of border_x
        prox.loc[i, 'prox_pos_x'] = 'out'
      elif -1 <= plate_x <= 1:
        prox.loc[i, 'prox_pos_x'] = 'in'
      if plate_z < 1.5: #below border_z
        prox.loc[i, 'prox_pos_z'] = 'out'
      elif plate_z > 3.5: #above border_z
        prox.loc[i, 'prox_pos_z'] = 'out'
      elif 1.5 <= plate_z <= 3.5:
        prox.loc[i, 'prox_pos_z'] = 'in'
      
      if plate_x > 0:
        prox.loc[i, 'prox_x'] = abs(plate_x-1)
      elif plate_x < 0:
        prox.loc[i, 'prox_x'] = abs(abs(plate_x)-1)
        
      if plate_z > 2.5:
        prox.loc[i, 'prox_z'] = abs(plate_z-3.5)
      elif plate_z < 2.5:
        prox.loc[i, 'prox_z'] = abs(plate_z-1.5)
    
    df = pd.concat([df, prox], axis=1)
    df.to_csv(exist_filepath,mode="w",encoding='utf-8-sig')
    

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
  # df = get_ump_list()
  # create_ump_history(df['Abbr'])
  # for i in range(len(df)):
  #   # push_ump_history(str(df.at[i,'Umpire']),str(df.at[i,'Abbr']))
  #   sanitize_ump_history(str(df.at[i,'Umpire']),str(df.at[i,'Abbr']))
  
  # sanitize_ump_history('Bill Miller','bill_miller')
  
  for season in range(2015,2022):
    evaluate_proximity(season)
