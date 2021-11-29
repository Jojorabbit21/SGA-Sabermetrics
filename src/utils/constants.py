from datetime import datetime, timedelta, timezone

# General Information
VERSION = "1.0.1"
CURRENT_YEAR = datetime.now().year
CURRENT_SEASON = "2022"

# Google Spreadsheets as Database
DB_NAME = "SGA Database"
DB_START_ROW = 1
DB_START_COL = 1

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

URL_LINEUPS = {
    "ODD": "https://www.lineups.com/mlb-odds",
    "PARK_FACTORS": "https://www.lineups.com/mlb/park-factors",
    "DC": "https://www.lineups.com/mlb/depth-charts"
}

URL_FP = {
    "LINEUP": "https://www.fantasypros.com/mlb/lineups/",
    "DC": "https://www.fantasypros.com/mlb/depth-charts.php"
}

URL_FGR = {
    "TEAM": "https://www.fangraphs.com/teams/",
    "TEAM_FIELDING": "https://www.fangraphs.com/leaders.aspx?pos=all&stats=fld&lg=all&qual=0&type=1&season=2021&month=0&season1=2018&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=&enddate=",
    "TEAM_PITCHING": [
        # 0 = Dashboard 1 = Batted Ball 2 = Pitch Value
        "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=8&season=2021&month=0&season1=2018&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2018-01-01&enddate=2021-12-31",
        "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=2&season=2021&month=0&season1=2018&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2018-01-01&enddate=2021-12-31",
        "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=7&season=2021&month=0&season1=2018&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2018-01-01&enddate=2021-12-31"
    ],
    "DC": "https://www.fangraphs.com/depth-charts/",
    "SPLIT": "https://www.fangraphs.com/leaders/splits-leaderboards?splitArr={}&splitArrPitch=&position={}&autoPt=true&splitTeams=false&statType=player&statgroup=1&startDate={}&endDate={}&players=&filter=&groupBy=season&sort=-1,1"
}

URL_MLB = { 
    "SCHEDULE": "https://www.mlb.com/schedule/",
    "LINEUP": "https://www.mlb.com/starting-lineups/"
}

URL_BP = {
    "LINEUP": "https://www.baseballpress.com/lineups/"
}

URL_RG = {
    "LINEUP": "https://rotogrinders.com/lineups/mlb?date=",
    "BvP": ["https://rotogrinders.com/game-stats/mlb-hitter?split=pitcher&pitcher_id=","&team_id="],
    "vR": "https://rotogrinders.com/game-stats/mlb-hitter?range=season&split=righty&team_id=",
    "vL": "https://rotogrinders.com/game-stats/mlb-hitter?range=season&split=lefty&team_id=",
    "aH": "https://rotogrinders.com/game-stats/mlb-hitter?range=season&split=home&team_id=",
    "aA": "https://rotogrinders.com/game-stats/mlb-hitter?range=season&split=away&team_id="
}

URL_NBC = {
    "DC": "https://www.nbcsportsedge.com/baseball/mlb/depth-charts"
}