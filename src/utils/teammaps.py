import pandas as pd

# No USE
def read_teammap():
    team_map = pd.read_csv('./static/teammap.csv',index_col=None)
    return team_map
