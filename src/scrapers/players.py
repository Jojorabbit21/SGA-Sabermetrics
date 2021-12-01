import requests
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from pybaseball import get_splits
from pybaseball import statcast_batter, statcast_pitcher
from pybaseball import statcast
from src.utils.playermaps import *
from src.utils.constants import *
from src.utils.dictionaries import *


# Play-by-play data of batter
def get_batter(playerid, start_date=None, end_date=None, pitcher_against=None):
    data = statcast_batter(start_dt=start_date, end_dt=end_date, player_id=playerid)
    
    # Columns: 
    # [pitch_type, game_date, release_speed, release_pos_x, release_pos_z, player_name, batter, pitcher, events, description, spin_dir, 
    # spin_rate_deprecated, break_angle_deprecated, break_length_deprecated, zone, des, game_type, stand, p_throws, home_team, away_team, type, 
    # hit_location, bb_type, balls, strikes, game_year, pfx_x, pfx_z, plate_x, plate_z, on_3b, on_2b, on_1b, outs_when_up, inning, inning_topbot, 
    # hc_x, hc_y, tfs_deprecated, tfs_zulu_deprecated, fielder_2, umpire, sv_id, vx0, vy0, vz0, ax, ay, az, sz_top, sz_bot, hit_distance_sc, 
    # launch_speed, launch_angle, effective_speed, release_spin_rate, release_extension, game_pk, 
    # pitcher.1, fielder_2.1, fielder_3, fielder_4, fielder_5, fielder_6, fielder_7, fielder_8, fielder_9, release_pos_y, 
    # estimated_ba_using_speedangle, estimated_woba_using_speedangle, woba_value, woba_denom, babip_value, iso_value, launch_speed_angle, 
    # at_bat_number, pitch_number, pitch_name, home_score, away_score, bat_score, fld_score, post_away_score, post_home_score, post_bat_score, 
    # post_fld_score, if_fielding_alignment, of_fielding_alignment, spin_axis, delta_home_win_exp, delta_run_exp]
    
    # 버릴 컬럼
    # [release_speed, release_pos_x, release_pos_z, description, spin_dir, 
    # spin_rate_deprecated, break_angle_deprecated, break_length_deprecated, zone, des, hit_location, balls, strikes, game_year, pfx_x, pfx_z, plate_x, plate_z, on_3b, on_2b, on_1b, outs_when_up, inning, inning_topbot,
    # hc_x, hc_y, tfs_deprecated, tfs_zulu_deprecated, fielder_2, umpire, sv_id, vx0, vy0, vz0, ax, ay, az, sz_top, sz_bot, hit_distance_sc, 
    # launch_speed, launch_angle, effective_speed, release_spin_rate, release_extension, game_pk, 
    # pitcher.1, fielder_2.1, fielder_3, fielder_4, fielder_5, fielder_6, fielder_7, fielder_8, fielder_9, release_pos_y, 
    # estimated_ba_using_speedangle, estimated_woba_using_speedangle, woba_value, woba_denom, babip_value, iso_value, launch_speed_angle, 
    # at_bat_number, pitch_number, pitch_name, home_score, away_score, bat_score, fld_score, post_away_score, post_home_score, post_bat_score, 
    # post_fld_score, if_fielding_alignment, of_fielding_alignment, spin_axis, delta_home_win_exp, delta_run_exp]]
    
    # if pitcher_against != None:
    #     debris = data[ data['pitcher'] != pitcher_against ].index
    #     if len(debris) > 0:
    #         data.drop(debris, inplace=True)
    #         data = data.reset_index(drop=True)
    
    data.to_csv('batter.csv')
    return data

# Play-by-play data of pitcher
def get_pitcher(playerid, start_date, end_date, batter_against=0):
    # 2015 at least
    data = statcast_pitcher(start_dt=start_date, end_dt=end_date, player_id=playerid)

    # Columns
    # 'pitch_type' 'game_date' 'release_speed' 'release_pos_x' 'release_pos_z' 'player_name' 'batter' 'pitcher' 'events' 'description' 'spin_dir'
    # 'spin_rate_deprecated' 'break_angle_deprecated' 'break_length_deprecated' 'zone' 'des' 'game_type' 'stand' 'p_throws' 'home_team' 'away_team'
    # 'type' 'hit_location' 'bb_type' 'balls' 'strikes' 'game_year' 'pfx_x' 'pfx_z' 'plate_x' 'plate_z' 'on_3b' 'on_2b' 'on_1b' 'outs_when_up'
    # 'inning' 'inning_topbot' 'hc_x' 'hc_y' 'tfs_deprecated' 'tfs_zulu_deprecated' 'fielder_2' 'umpire' 'sv_id' 'vx0' 'vy0' 'vz0' 'ax'
    # 'ay' 'az' 'sz_top' 'sz_bot' 'hit_distance_sc' 'launch_speed' 'launch_angle' 'effective_speed' 'release_spin_rate' 'release_extension'
    # 'game_pk' 'pitcher.1' 'fielder_2.1' 'fielder_3' 'fielder_4' 'fielder_5' 'fielder_6' 'fielder_7' 'fielder_8' 'fielder_9' 'release_pos_y'
    # 'estimated_ba_using_speedangle' 'estimated_woba_using_speedangle' 'woba_value' 'woba_denom' 'babip_value' 'iso_value' 'launch_speed_angle' 'at_bat_number' 'pitch_number' 'pitch_name' 'home_score' 'away_score'
    # 'bat_score' 'fld_score' 'post_away_score' 'post_home_score' 'post_bat_score' 'post_fld_score' 'if_fielding_alignment' 'of_fielding_alignment' 'spin_axis' 'delta_home_win_exp' 'delta_run_exp'

    # events = { 'strikeout', 'field_out', '}
    # data['type']=='X' => Hit, 'S' => 'Strike', 'B' => 'Ball
    # AVG => 안타/타수

    if batter_against != 0:
        debris = data[ data['batter'] != batter_against ].index
        if len(debris) > 0:
            data.drop(debris, inplace=True)
            data = data.reset_index(drop=True)
        
    return data

def get_statcast(start_dt='2017-03-01', end_dt='2021-11-31'):
    df = statcast(start_dt=start_dt, end_dt=end_dt)
    return df