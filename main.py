import pandas as pd

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
    # pd.set_option('display.max_rows',999)
    
    ### -> 매일 돌릴 필요 없는 모듈
    # r = get_team_roasters()
    
    ################## --- INITIATE --- ###################
    ############ Get Park Factors (Done)
    # park_factors = get_park_factors() #-> 완료
    # upload_dataframes(park_factors, 'PA')
    # ############ Get Team Depthcharts (Done)
    # d = get_team_depthcharts() #-> 완료
    # upload_dataframes(d, 'DP')
    # ############ Get General Team Stats
    # team = get_team_batting_table(start_season=2015,end_season=2021) #-> 완료
    # upload_dataframes(team, 'TB')
    # f = get_team_fielding_table() #-> 완료
    # upload_dataframes(f, 'TF')
    # pp = get_team_pitching_table(2015, 2021) # -> 완료
    # # upload_dataframes(pp, 'TP') 
    
    ################################################################################# WIP

    # ############ Get Match and Lineups
    # matches, players = get_matches('2021-08-03')
    # clear_sheet('M')
    # upload_dataframes(matches,'M')
    
    # ############ Get Team H2H by Seasons
    # for i in range(0, len(matches)):
    #     visit = matches.loc[[i],['Visitor']].to_numpy()
    #     home = matches.loc[[i], ['Home']].to_numpy()
    #     visit = str(visit[0][0])
    #     home = str(home[0][0])
    #     h2h_p = get_head_to_head(visit,home,2021,log_type="pitching")
    #     h2h_b = get_head_to_head(visit,home,2021,log_type="batting")
    #     upload_dataframes(h2h_p, 'TH_P')
    #     upload_dataframes(h2h_b, 'TH_B')
    #     -> dataframe 하나로 머지해서 업로드하는걸로 하자
    
    
    # print(get_teambatting_split(DICT_TEAMNAMES['ARI'][16], 'L'))
    # get_fgr_split('COL','B','STL')
        
    # Get Player statcast_batting and pitchervsbatter
    pitcherid = find_player(source='BBREF',full_name="Albert Abreu")




    


if __name__ == "__main__":
    main()
