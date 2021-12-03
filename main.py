import pandas as pd
from datetime import datetime, timedelta, timezone
from time import sleep, strptime
from tqdm import tqdm, trange

from src.refiners.time import refine_gametime
from src.scrapers.depthchart import *
from src.scrapers.parkfactors import *
from src.scrapers.matches import *
from src.scrapers.players import *
from src.scrapers.teams import *

from src.utils.dictionaries import *
from src.utils import constants, teammaps, playermaps

from src.uploaders.uploader import *



def main():
    
    # pd.set_option('display.max_columns',50)
    # pd.set_option('display.max_columns',999)
    pd.set_option('display.max_rows',999)
    
    # print('Initiating')
    # print("Getting Player Roaster")
    # rb, rp = get_team_roasters()
    # upload_dataframes(rb, 'B')
    # upload_dataframes(rp, 'P')

    # print("Getting Park Factors")
    # park_factors = get_park_factors()
    # upload_dataframes(park_factors, 'PA')
    
    # print("Getting Depth Charts")
    # d = get_team_depthcharts()
    # upload_dataframes(d, 'DP')
    
    # print("Get Batting Table")
    # team = get_team_batting_table(2017,2021)
    # upload_dataframes(team, 'TB')
    
    # print("Get Fielding Table")
    # f = get_team_fielding_table()
    # upload_dataframes(f, 'TF')
    
    # print("Get Pitching Table")
    # pp = get_team_pitching_table(2015, 2021)
    # upload_dataframes(pp, 'TP') 

    # print("Get Matchups/Lineups")
    matches, players = get_matches('2021-08-03')
    clear_sheet('M')
    upload_dataframes(matches,'M')
    h2h_p = pd.DataFrame()
    h2h_b = pd.DataFrame()
    split_b = pd.DataFrame()
    split_p = pd.DataFrame()
    for i in tqdm(range(0, len(matches)),desc="Getting H2H/Splits"):
        visit = matches.loc[[i],['Visitor']].to_numpy()
        home = matches.loc[[i], ['Home']].to_numpy()
        # visitph = matches.loc[[i], ['Visitor Pitcher Hand']].to_numpy()
        # homeph = matches.loc[[i], ['Home Pitcher Hand']].to_numpy()
        # visitph = str(visitph[0][0])
        # homeph = str(homeph[0][0])
        visit = str(visit[0][0])
        home = str(home[0][0])
        h2h_pp = get_head_to_head(visit,home,2021,log_type="pitching")
        h2h_bb = get_head_to_head(visit,home,2021,log_type="batting")
        h2h_p = pd.concat([h2h_p, h2h_pp], axis=0)
        h2h_b = pd.concat([h2h_b, h2h_bb], axis=0)
    #     split_vb = get_fgr_split(visit, 'B', home, hand=None, opphand=homeph, home='A')
    #     split_b = pd.concat([split_b, split_vb], axis=0)
    #     split_vb = get_fgr_split(home, 'B', visit, hand=None, opphand=visitph, home='A')
    #     split_b = pd.concat([split_b, split_vb], axis=0)
    #     split_vp = get_fgr_split(visit, 'P', home, hand=None, opphand='L', home='A')
    #     split_p = pd.concat([split_p, split_vp], axis=0)
    #     split_vp = get_fgr_split(visit, 'P', home, hand=None, opphand='R', home='A')
    #     split_p = pd.concat([split_p, split_vp], axis=0)
    #     split_vp = get_fgr_split(home, 'P', visit, hand=None, opphand='L', home='H')
    #     split_p = pd.concat([split_p, split_vp], axis=0)
    #     split_vp = get_fgr_split(home, 'P', visit, hand=None, opphand='R', home='H')
    #     split_p = pd.concat([split_p, split_vp], axis=0)
    clear_sheet('TH_P')
    clear_sheet('TH_B')
    # clear_sheet('PB')
    # clear_sheet('PP')
    upload_dataframes(h2h_p, 'TH_P')
    upload_dataframes(h2h_b, 'TH_B')
    # upload_dataframes(split_b, 'PB')
    # upload_dataframes(split_p, 'PP')
    
    # Get Splits
    # Order
    # batter split : pitchers hand + home/away
    # pitcher split : vLHH + home/away & vRHH + home/away
    # total 3 dataframes to merge
    
    # split = pd.DataFrame()
    # df = get_fgr_split('ARI','P',opp='PHI', hand='R', opphand='L', home='A')
    # split = pd.concat([split,df],axis=0)
    # df = get_fgr_split('PHI','P',opp='ARI', hand='L', opphand='L', home='H')
    # split = pd.concat([split,df],axis=0)
    # print(split)
    
    
if __name__ == "__main__":
    main()
