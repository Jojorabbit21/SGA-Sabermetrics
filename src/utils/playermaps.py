from numpy import e
import pandas as pd
import math

# No USE
def read_playermap():
    pid_map = pd.read_csv('./static/playeridmap.csv',index_col=None)
    inactives = pid_map[ pid_map['ACTIVE'] == 'N' ].index
    pid_map.drop(inactives, inplace=True)
    pid_map = pid_map.reset_index(drop=True)
    return pid_map

def find_player(source=['BBREF','MLB','FGR','RETRO', 'ESPN'], full_name:str=None, first_name:str=None, last_name:str=None):
    player_map = read_playermap()
    if len(full_name) > 0:
        target_name = full_name
    else:
        target_name = first_name + " " + last_name
    if source == 'BBREF':
        target = 'BREFID'
    elif source == 'MLB':
        target = 'MLBID'
    elif source == 'FGR':
        target = 'IDFANGRAPHS'
    elif source == 'RETRO':
        target = 'RETROID'
    elif source == 'ESPN':
        target = 'ESPNID'
        
    player = player_map[player_map['PLAYERNAME'] == target_name]
    if not player.empty:
        playerid = str(player_map.loc[player.index[0], target])
    else:  
        playerid = None
    return playerid

def find_umpire(full_name):
    # Still Thinkin'
    pass
