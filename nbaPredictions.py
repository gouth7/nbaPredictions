import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import time
from selenium import webdriver

teamNames = {
    "Hawks" : "ATL",
    "Celtics" : "BOS",
    "Nets" : "BKN",
    "Hornets" : "CHA",
    "Bulls" : "CHI",
    "Caveliers" : "CLE",
    "Mavericks" : "DAL",
    "Nuggets" : "DEN",
    "Pistons" : "DET",
    "Warriors" : "GS",
    "Rockets" : "HOU",
    "Pacers" : "IND",
    "Clippers" : "LAC",
    "Lakers" : "LAL",
    "Grizzlies" : "MEM",
    "Heat" : "MIA",
    "Bucks" : "MIL",
    "Timberwolves" : "MIN",
    "Pelicans" : "NO",
    "Knicks" : "NY",
    "Thunder" : "OKC",
    "Magic" : "ORL",
    "76ers" : "PHI",
    "Suns" : "PHX",
    "Blazers" : "POR",
    "Kings" : "SAC",
    "Spurs" : "SA",
    "Raptors" : "TOR",
    "Jazz" : "UTA",
    "Cavaliers" : "CLE",
    "Wizards" : "WSH"
}


def read538():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("/Users/gouth/Downloads/chromedriver", options=options)
    driver.get("https://projects.fivethirtyeight.com/2020-nba-predictions/games/")
    more_buttons = driver.find_elements_by_class_name("btn-cta")
    for x in range(len(more_buttons)):
      if more_buttons[x].is_displayed():
          driver.execute_script("arguments[0].click();", more_buttons[x])
          time.sleep(2)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source)
    return soup

#def find_days():

ft8 = pd.DataFrame(columns=['winner','loser','spread','winnerScore','loserScore', 'date', 'dbspread'])
db = pd.DataFrame(columns=['team1', 'team2', 'spread', 'date'])

five_total = {}
teams = {}
predictions = {}
i = 0
soup = read538()
completed = soup.find_all('div', class_='completed-day')[0]
print("completed \n\n" + str(completed))
day = completed.find_all('section', class_='day')
print(soup)

for d in day:
    dateRegex  = re.compile(r'(?<=\w{3}\. )\d\d?')
    daytext = str(d)
    date = dateRegex.findall(daytext)
    print("\n\ndate: " + str(date))
    print("day \n\n" + str(d))
    games = d.find_all('tbody', class_='ie10up')
    for g in games:
      #spreadRegex = re.compile(r'(?<="td number spread"> ).+')
      spreadRegex = re.compile(r'(?<="td number spread"> )-?\d+\.?\d?')
      spread_text = g.find_all('td', class_='td number spread')
      spreadlist = []
      for spread in spread_text:
        spread_str = str(spread)
        spreadlist.append(spreadRegex.findall(spread_str))
      game = str(g)
      print("game \n\n" + game)
      loserScoreRegex = re.compile(r'[a-z]{4,}', re.IGNORECASE)
      teamsRegex = re.compile(r'(?<=td text team )\w*')
      winnerRegex = re.compile(r'(?<=td text team winner )\w{1,3}')
      loserRegex = re.compile(r'(?<=td text team loser )\w{1,3}')
      #spreadRegex = re.compile(r'(?<="td number spread"> )-?\d+\.?\d?')
      loserScoreRegex = re.compile(r'(?<=score loser">)\d+')
      winnerScoreRegex = re.compile(r'(?<=score winner">)\d+')

      spreadOrder = teamsRegex.findall(game)
      winner = (winnerRegex.findall(game))
      loser = (loserRegex.findall(game))
      winnerScore = (winnerScoreRegex.findall(game))
      loserScore = (loserScoreRegex.findall(game))
      print(spreadlist)
      # if the spread is 0
      if spreadlist[0] == spreadlist[1]:
          spreadlist[0] = "0"
      if spreadOrder[0] == 'loser':
          if not spreadlist[0]:
              spread = float(spreadlist[1][0]) * -1
          else:
              spread = float(spreadlist[0][0])
      else:
          if not spreadlist[0]:
              spread = float(spreadlist[1][0])
          else:
              spread = float(spreadlist[0][0]) * -1

      ft8 = ft8.append({'winner':winner, 'loser':loser, 'spread':spread, 'winnerScore':int(winnerScore[0]), 'loserScore':int(loserScore[0]), 'date':int(date[0])}, ignore_index=True)
#spread is from losers perspective
print(ft8)

#------------------DonBest-------------------------
year = '2019'
day = 22
month = 10
stop = 0
url = "http://www.donbest.com/nba/odds/20191122.html"
retryCounter = 0

while not stop:
    try:
        time.sleep(4)
        if (day<10):
            day_str = '0' + str(day)
        else:
            day_str = str(day)
        new_url = "http://www.donbest.com/nba/odds/{}{}{}.html".format(year,month,day_str)
        print("\n url: " + new_url)
        page = requests.get(new_url)
        print(page.status_code)
        soup = BeautifulSoup(page.content, 'html.parser')
        names = soup.findAll('span', attrs={'oddsTeamWLink'})
        opener = soup.findAll('td', attrs={'alignRight oddsOpener'})
        #print("-------- \n" + str(opener) + "\n\n")
        spreadRegex = re.compile(r'(\d+\.\d)|PK')
        spreadSignRegex = re.compile(r'(\+|\-)|PK')
        pattern = re.compile(r'(?<=\s)\S*$', re.IGNORECASE)
        teams = []
        spreads = []
        spreadSignList = []
        for team in names:
            result_team_names_don = pattern.findall(team.get_text())
            teams.append(str(result_team_names_don[0]))
        for item in opener:
            spread = spreadRegex.findall(item.get_text())
            spreadSign = spreadSignRegex.findall(item.get_text())
            spreadSignList.append(spreadSign[0])
            spreads.append(spread[0])
            spreads.append(spread[1])
    except Exception as err:
        print(err)
    actualSpread = []
    for i in range(0, len(spreads), 2):
        if (str(spreadSignList[int(i/2)]) == '-'):
            neg = -1
        else:
            neg = 1
        if (str(spreads[i]) == ''):
            spreads[i] = 0.0
        if (str(spreads[i+1]) == ''):
            spreads[i] = 0.0
        if (float(spreads[i]) < 50):
            val = float(spreads[i]) * neg
            actualSpread.append(val)
        else:
             val = -1  * float(spreads[i+1]) * neg
             actualSpread.append(val)
    # spread is team 1's perspective
    print(str(teams))
    print(str(actualSpread))
    print(len(teams))
    #if (len(teams) != len(ft8.loc[ft8.date==day])):
    if (len(teams) == 0):
        retryCounter+=1
        continue
    else:
        retryCounter = 0
    if (len(actualSpread) != (len(teams)/2)):
        continue
    if (retryCounter == 5):
        day += 1
    for i in range(0, len(teams), 2):
        db = db.append({'team1':teams[i], 'team2':teams[i+1], 'spread':float(actualSpread[int(i/2)]), 'date':day}, ignore_index=True)
    #print(db)
    day+=1
    if (day==32):
        month+=1
        day = 1
    if ((day == 31) and (month == 12)):
        stop = 1
print(db)
counter = 0
for ft8row in ft8.iterrows():
    for dbrow in db.iterrows():
        #print(ft8row[1]['winner'][0] + teamNames[dbrow[1]['team1']])
        if (dbrow[1]['date'] != ft8row[1]['date']):
            continue
        if ((ft8row[1]['winner'][0] == teamNames[dbrow[1]['team1']]) & (ft8row[1]['loser'][0] == teamNames[dbrow[1]['team2']])):
            ft8.loc[counter, 'dbspread'] = dbrow[1]['spread'] *-1
        if ((ft8row[1]['loser'][0] == teamNames[dbrow[1]['team1']]) & (ft8row[1]['winner'][0] == teamNames[dbrow[1]['team2']])):
            ft8.loc[counter, 'dbspread'] = dbrow[1]['spread']
    counter+=1


#db spread is from perspective of loser. If negative, loser was supposed to win.


# json = json.dumps(five_total)
# f = open("nba.json","w")
# f.write(json)
# f.close()
ft8['diff'] = ft8.winnerScore - ft8.loserScore

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
  print(ft8)

print("Games vegas picked wrong")
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
  a = ft8.loc[(ft8.dbspread < 0) & (ft8.spread > 0)]
  print(a)
  print(len(a))

print("games five thirty eight picked wrong")
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
  b = ft8.loc[(ft8.spread < 0) & (ft8.dbspread > 0)]
  print(b)
  print(len(b))


print("games they agree on")
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
   b = ft8.loc[(abs(ft8.spread - ft8.dbspread) < 1)]
   c = b.loc[(abs(b.spread - b.dbspread) > 0)]
   print(c)
   print(len(c))
