
import pandas as pd
from pybaseball import get_splits
from pybaseball import statcast_batter, statcast_pitcher
from src.utils.playermaps import *

def test():
    df, player_info_dict = get_splits('troutmi01', player_info=True)
    # Season totals, platoon splits, home/away, vs. Power/Finesse Pitchers vs. Ground Ball/Fly Ball Pitchers, Opponent, Game Conditions, Ballparks
    # print(df)
    df2 = get_splits('lestejo01', pitching_splits=True)
    # Season totals, platoon splits, home/away, pitching role, run support, Clutch stats, pitch count, days of rest, hit location, opponent, game conditions, ballparks, by umpire(심판 데이터를 나중에 따로 뽑아서 여기서 추출)
    print(df2)


def get_batter(playerid, start_date, end_date, pitcher_against=0):
    data = statcast_batter(start_dt=start_date, end_dt=end_date, player_id=playerid)
    
    # statcast_batter 에는 상대 pitcher playerid가 나온다. 이를 통해서 상대 선발투수와의 히스토리를 알 수 있다.
    # 나머지 필요 없는 columns 다 덜어내면 무겁지 않을 것으로 보임.
    
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
    
    if pitcher_against != 0:
        debris = data[ data['pitcher'] != pitcher_against ].index
        if len(debris) > 0:
            data.drop(debris, inplace=True)
            data = data.reset_index(drop=True)
        
    return data

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


# https://rotogrinders.com/game-stats/mlb-hitter?split=pitcher&pitcher_id=13434&team_id=119
# PvB 이곳에서 데이터 뽑으면 될 것으로 보임. opp_pitcher_id & team_id 필요 :: div > div > div.splits > ul > li:nth-child(1) > a['href']