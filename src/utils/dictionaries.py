from typing import SupportsAbs

'''
[참고용]
National League
    West = SF, LAD, SD, COL, ARI
    East = ATL, PHI, NYM, MIA, WSH
    Central = MIL, STL, CIN, CHC, PIT
American League
    East = TB, BOS, NYY, TOR, BAL
    Central = CWS, CLE, DET, KC, MIN
    West = HOU, SEA, OAK, LAA, TEX
'''

LIST_TEAMS = [
    "ARI","ATL","BAL","BOS","CHC","CHW","CIN","CLE","COL","DET","HOU","KC","LAA","LAD","MIA",
    "MIL","MIN","NYM","NYY","OAK","PHI","PIT","SD","SEA","SF","STL","TB","TEX","TOR","WAS"
]

DICT_SOURCE = {
    "SFBBTEAM": 0,
    "FDTEAM": 1,
    "DKTEAM": 2,
    "BBREFTEAM": 3,
    "YAHOOTEAM": 4,
    "FANPROSTEAM": 5,
    "BASEBALLPRESSTEAM": 6,
    "FANGRAPHSTEAM": 7,
    "ESPNTEAM": 8,
    "BPTEAM": 9,
    "ROTOWIRETEAM": 10,
    "ROSTERRESOURCEURL": 11,
    "RETROSHEET": 12,
    "FANGRAPHSABBR": 13,
    "FANGRAPHSRR": 14,
    "PARK": 15,
    "ROTOGRINDERTEAMID": 16
}

DICT_TEAMNAMES = {
    # SFBB = SmartFantasyBaseball 
    # FD = FanDuel
    # DK = DraftKings
    # BBREF = Baseball-ReferenceError
    # YAHOO = Yahoo Sports
    # FANPROS = FantasyPros
    # BASEBALLPRESS = Baseball Press
    # ROTOWIRE = Rotowire
    # FANGRAPHS = Fangraphs
    # ESPN = ESPN
    # BP = Baseball Prospectus
    # RETROSHEET = Retrosheet

    "ARI": ["ARI","ARI","ARI","ARI","ARI","ARI","ARI","Diamondbacks","ARI","ARI","ARI","MLB-ARIZONA-DIAMONDBACKS","ARI","ARI","diamondbacks", "Chase Field", "109"],
    "ATL": ["ATL","ATL","ATL","ATL","ATL","ATL","ATL","Braves","ATL","ATL","ATL","MLB-ATALANTA-BRAVES","ATL","ATL","braves", "Truist Park", "110"],
    "BAL": ["BAL","BAL","BAL","BAL","BAL","BAL","BAL","Orioles","BAL","BAL","BAL","MLB-BALTIMORE-ORIOLES","BAL","BAL","orioles", "Oriole Park at Camden Yards", "96"],
    "BOS": ["BOS","BOS","BOS","BOS","BOS","BOS","BOS","Red Sox","BOS","BOS","BOS","MLB-BOSTON-RED-SOX","BOS","BOS","red-sox", "Fenway Park", "95"],
    # CHC CHN
    "CHC": ["CHC","CHC","CHC","CHC","CHC","CHC","CHC","Cubs","CHC","CHN","CHC","MLB-CHICAGO-CUBS","CHN","CHC","cubs", "Wrigley Field", "111"],
    # CHW CWS CHA
    "CHW": ["CWS","CWS","CWS","CHW","CWS","CWS","CWS","White Sox","CHW","CHA","CWS","MLB-CHICAGO-WHITE-SOX","CHA","CHW","white-sox", "Guaranteed Rate Field", "97"],
    "CIN": ["CIN","CIN","CIN","CIN","CIN","CIN","CIN","Reds","CIN","CIN","CIN","MLB-CINCINNATI-REDS","CIN","CIN","reds", "Great American Ball Park", "112"],
    "CLE": ["CLE","CLE","CLE","CLE","CLE","CLE","CLE","Indians","CLE","CLE","CLE","MLB-CLEVELAND-INDIANS","CLE","CLE","cleveland", "Progressive Field", "98"],
    "COL": ["COL","COL","COL","COL","COL","COL","COL","Rockies","COL","COL","COL","MLB-COLORADO-ROCKIES","COL","COL","rockies", "Coors Field", "113"],
    "DET": ["DET","DET","DET","DET","DET","DET","DET","Tigers","DET","DET","DET","MLB-DETROIT-TIGERS","DET","DET","tigers", "Comerica Park", "99"],
    "HOU": ["HOU","HOU","HOU","HOU","HOU","HOU","HOU","Astros","HOU","HOU","HOU","MLB-HOUSTON-ASTROS","HOU","HOU","astros", "Minute Maid Park", "115"],
    # KC KAN KCR KCA
    "KC": ["KC","KAN","KC","KCR","KC","KC","KC","Royals","KC","KCA","KC","MLB-KANSAS-CITY-ROYALS","KCA","KC","royals", "Kauffman Stadium", "100"],
    # LAA ANA
    "LAA": ["LAA","LAA","LAA","LAA","LAA","LAA","LAA","Angels","LAA","ANA","LAA","MLB-LOS-ANGELES-ANGELS","ANA","LAA","angels", "Angel Stadium of Anaheim", "101"],
    # LAD LAN
    "LAD": ["LAD","LOS","LAD","LAD","LAD","LAD","LAD","Dodgers","LAD","LAN","LAD","MLB-LOS-ANGELES-DODGERS","LAN","LAD","dodgers", "Dodger Stadium", "116"],
    "MIA": ["MIA","MIA","MIA","MIA","MIA","MIA","MIA","Marlins","MIA","MIA","MIA","MLB-MIAMI-MARLINS","MIA","MIA","marlins", "Marlins Park", "114"],
    "MIL": ["MIL","MIL","MIL","MIL","MIL","MIL","MIL","Brewers","MIL","MIL","MIL","MLB-MILWAUKEE-BREWERS","MIL","MIL","brewers", "Miller Park", "117"],
    "MIN": ["MIN","MIN","MIN","MIN","MIN","MIN","MIN","Twins","MIN","MIN","MIN","MLB-MINNESOTA-TWINS","MIN","MIN","twins", "Target Field", "102"],
    # NYM NYN
    "NYM": ["NYM","NYM","NYM","NYM","NYM","NYM","NYM","Mets","NYM","NYN","NYM","MLB-NEW-YORK-METS","NYN","NYM","mets", "Citi Field", "118"],
    # NYY NYA
    "NYY": ["NYY","NYY","NYY","NYY","NYY","NYY","NYY","Yankees","NYY","NYA","NYY","MLB-NEW-YORK-YANKEES","NYA","NYY","yankees", "Yankee Stadium", "103"],
    "OAK": ["OAK","OAK","OAK","OAK","OAK","OAK","OAK","Athletics","OAK","OAK","OAK","MLB-OAKLAND-ATHLETICS","OAK","OAK","athletics","RingCentral Coliseum", "104"],
    "PHI": ["PHI","PHI","PHI","PHI","PHI","PHI","PHI","Phillies","PHI","PHI","PHI","MLB-PHILADELPHIA-PHILLIES","PHI","PHI","phillies","Citizens Bank Park", "119"],
    "PIT": ["PIT","PIT","PIT","PIT","PIT","PIT","PIT","Pirates","PIT","PIT","PIT","MLB-PITTSBURGH-PIRATES","PIT","PIT","pirates","PNC Park", "120"],
    # SD SDP SDN
    "SD": ["SD","SDP","SD","SDP","SD","SD","SD","Padres","SD","SDN","SD","MLB-SAN-DIEGO-PADRES","SDN","SD","padres","PETCO Park", "121"],
    "SEA": ["SEA","SEA","SEA","SEA","SEA","SEA","SEA","Mariners","SEA","SEA","SEA","MLB-SEATTLE-MARINERS","SEA","SEA","mariners","T-Mobile Park", "105"],
    # SF SFG SFN
    "SF": ["SF","SFG","SF","SFG","SF","SF","SF","Giants","SF","SFN","SF","MLB-SAN-FRANCISCO-GIANTS","SFN","SF","giants","Oracle Park", "122"],
    # STL SLN
    "STL": ["STL","STL","STL","STL","STL","STL","STL","Cardinals","STL","STL","STL","MLB-ST-LOUIS-CARDINALS","SLN","STL","cardinals","Busch Stadium", "123"],
    # TB TAM TBR TBA
    "TB": ["TB","TAM","TB","TBR","TB","TB","TB","Rays","TB","TBA","TB","MLB-TAMPA-BAY-RAYS","TBA","TB","rays","Tropicana Field", "106"],
    "TEX": ["TEX","TEX","TEX","TEX","TEX","TEX","TEX","Rangers","TEX","TEX","TEX","MLB-TEXAS-RANGERS","TEX","TEX","rangers","Globe Life Field", "107"],
    "TOR": ["TOR","TOR","TOR","TOR","TOR","TOR","TOR","Blue Jays","TOR","TOR","TOR","MLB-TORONTO-BLUE-JAYS","TOR","TOR","blue-jays","Rogers Centre", "108"],
    # WAS WSH WSN
    "WAS": ["WAS","WAS","WAS","WSN","WAS","WSH","WSH","Nationals","WSH","WAS","WAS","MLB-WASHINGTON-NATIONALS","WAS","WAS","nationals","Nationals Park", "124"]
}

DICT_SANITIZE = {
    "CHN": "CHC",
    "CWS": "CHW",
    "CHA": "CHW",
    "KAN": "KC",
    "KCR": "KC",
    "KCA": "KC",
    "ANA": "LAA",
    "LAN": "LAD",
    "NYN": "NYM",
    "NYA": "NYY",
    "SDP": "SD",
    "SDN": "SD",
    "SFG": "SF",
    "SFN": "SF",
    "SLN": "STL",
    "TAM": "TB",
    "TBR": "TB",
    "TBA": "TB",
    "WSH": "WAS",
    "WSN": "WAS"
}

DICT_BP_LINEUP = {
    "D-backs": "ARI",
    "Diamondbacks": "ARI",
    "Braves": "ATL",
    "Orioles": "BAL",
    "Red Sox": "BOS",
    "Cubs": "CHC",
    "White Sox": "CHW",
    "Reds": "CIN",
    "Indians": "CLE",
    "Guardians": "CLE",
    "Rockies": "COL",
    "Tigers": "DET",
    "Astros": "HOU",
    "Royals": "KC",
    "Angels": "LAA",
    "Dodgers": "LAD",
    "Marlins": "MIA",
    "Twins": "MIN",
    "Brewers": "MIL",
    "Mets": "NYM",
    "Yankees": "NYY",
    "Athletics": "OAK",
    "Phillies": "PHI",
    "Pirates": "PIT",
    "Padres": "SD",
    "Giants": "SF",
    "Mariners": "SEA",
    "Cardinals": "STL",
    "Rays": "TB",
    "Rangers": "TEX",
    "Blue Jays": "TOR",
    "Nationals": "WAS"
}

