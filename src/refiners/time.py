import datetime

def refine_gametime(dt:str):
  dt = dt.replace(' ET','')
  from_format = '%Y-%m-%d %I:%M %p'
  date_temp = datetime.datetime.strptime(dt, from_format) + datetime.timedelta(hours=14)
  date_formatted = date_temp.strftime('%Y-%m-%d %H:%M')
  return date_formatted