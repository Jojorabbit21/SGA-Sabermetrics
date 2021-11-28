import pandas as pd

from src.scrapers.depthchart import *
from src.scrapers.parkfactors import *
from src.scrapers.matches import *
from src.scrapers.players import *
from src.scrapers.teams import *

from src.utils.dictionaries import *
from src.utils import constants, teammaps, playermaps


def main():
    # pd.set_option('display.max_columns',50)
    pd.set_option('display.max_columns',999)
    # pd.set_option('display.max_rows',999)
    
    ### -> 매일 돌릴 필요 없는 모듈
    # get_team_roasters()
    
    ################## --- INITIATE --- ###################
    # Get Park Factors
    # park_factors = get_park_factors()
    # Get Team Depthcharts
    # d = get_team_depthcharts()
    
    # get_pitcher_splits()
    
    # Get Match and Lineups
    # matches, players = get_matches('2021-08-03')
    
    # Get Player statcast_batting and pitchervsbatter
    # pitcherid = find_player("Gerrit Cole")
    # # batterid = find_player("Ji-Man Choi")
    # data = get_pitcher(pitcherid, '2017-04-01', '2021-11-01')

    # Get team stats
    # team = get_team_batting('ATL') 
    # team = get_team_batting_table(start_season=2021,end_season=2021)

    # get_team_fielding('STL',2018, 2021)
    # f = get_team_fielding_table(2018,2021)
    
    # p = get_team_pitching('STL', 2018, 2021)
    # pp = get_team_pitching_table(2018, 2021)
    
    # Get Team H2H by Seasons
    # h2h = get_head_to_head("ATL","PHI",2021,log_type="pitching")
    


if __name__ == "__main__":
    main()
