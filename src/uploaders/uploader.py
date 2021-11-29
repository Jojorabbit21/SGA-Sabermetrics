import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from datetime import datetime, timedelta, timezone

from src.utils.constants import *
from src.utils.dictionaries import *

def upload_dataframes(data, keyword):
  gc = gspread.service_account(filename="./src/uploaders/agent.json")
  sh = gc.open(DB_NAME).worksheet(DB_SHEETS[keyword])
  set_with_dataframe(sh, data, row=DB_START_ROW, col=DB_START_COL, include_index=False, include_column_header=True)

def clear_sheet(sheetname):
  gc = gspread.service_account(filename="./src/uploaders/agent.json")
  sh = gc.open(DB_NAME).worksheet(DB_SHEETS[sheetname])
  sh.clear()