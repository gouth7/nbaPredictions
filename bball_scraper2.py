import requests
from bs4 import BeautifulSoup
import re
import json
#print(soup.prettify())


page = requests.get("https://projects.fivethirtyeight.com/2018-nba-predictions/games/?ex_cid=rrpromo")
print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')
five_total = {}
teams = {}
predictions = {}
i = 0

day = soup.find_all('div', class_='completed-day')[0] # jan 1
games = day.find_all('tbody', class_='ie10up') #game 1 day 1
for game in games:
  pattern = re.compile(r'[a-z]{4,}', re.IGNORECASE)
  pattern2 = re.compile(r'..(?=%)')
  result_names = pattern.findall(game.get_text())
  result_predictions = pattern2.findall(game.get_text())
  #accomodate Trail Blazers because two words and 76ers because numbers
  if len(result_names)==1:
      teams[i] = [result_names[0], '76ers']
  elif len(result_names)>2:
      if result_names[0] == 'Trail':
          teams[i] = ['Blazers', result_names[2]]
      else:
          teams[i] = [result_names[0], 'Blazers']
  else:
      teams[i] = result_names

  predictions[i] = result_predictions
  i +=1
five_total['teams'] = teams
five_total['predictions'] = predictions
#Print Each completed Game from FiveThirtyEight
#for game in five_total['teams']:
#    print("----game----")
#    print(five_total['teams'][game][0], "vs", five_total['teams'][game][1])

#------------------DonBest-------------------------
year = '8'
day = '02'
month = '01'
stop = 0
url = "http://www.donbest.com/nba/odds/money-lines/20180102.html"
five_total['winner'] = {}

while not stop:
    try:
        new_url = url[:47] + year + month + day + url[52:]
        print(new_url)
        page = requests.get(new_url)
        print(page.status_code)
        soup = BeautifulSoup(page.content, 'html.parser')
        names = soup.findAll('span', attrs={'oddsTeamWLink'})

        team_list = []
        odds_teams = {}
        Don_total = {}
        pattern = re.compile(r'(?<=\s)\S*$', re.IGNORECASE)
        #Put team names into list
        for team in names:
            result_team_names_don = pattern.findall(team.get_text())
            team_list.append(result_team_names_don[0])
        #Format team names into games
        i =0
        while(1):
            if i+1 >= len(team_list):
                break;
            odds_teams[i//2] = [team_list[i], team_list[i+1]]
            i = i+2
        Don_total['teams'] = odds_teams
        #Find Scores
        winner = {}
        pattern = re.compile(r'\d{4,6}(?=\sFINAL)', re.IGNORECASE)
        scores = soup.findAll('div', attrs={'odds_gamesHolder'})
        result_scores_don = pattern.findall(scores[0].get_text())

        #determine winner
        i=0
        for score in result_scores_don:
            if len(score)==4:
                if (score[0]>score[2]) or (score[0]==score[2] and score[1]>score[3]):
                    winner[i] = 0
                elif (score[0]<score[2]) or (score[0]==score[2] and score[1]<score[3]):
                    winner[i] = 1
            if len(score) == 5:
                if score[0] == 1:
                    winner[i] = 0
                else:
                    winner[i] = 1
            if len(score) == 6:
                if (score[1]>score[4]) or (score[1]==score[4] and score[2]>score[5]):
                    winner[i] = 0
                elif (score[1]<score[4]) or (score[1]==score[4] and score[2]<score[5]):
                    winner[i] = 1
            i+=1
        Don_total['winner'] = winner
        #print(Don_total)

        for don_team in Don_total['teams']:
            for five_team in five_total['teams']:
                try:
                    if (five_total['winner'][five_team]):
                        continue
                except:
                    pass
                if (five_total['teams'][five_team][0] == Don_total['teams'][don_team][0] and five_total['teams'][five_team][1] == Don_total['teams'][don_team][1]):
                    five_total['winner'][five_team] = Don_total['winner'][don_team]
                    break
                elif (five_total['teams'][five_team][0] == Don_total['teams'][don_team][1] and five_total['teams'][five_team][1] == Don_total['teams'][don_team][0]):
                    five_total['winner'][five_team] = Don_total['winner'][don_team]^1
                    break
        #print(five_total)


        day = int(day) - 1
        if day==0:
            day = 30
            month = int(month) - 1
            if not month%2:
                day = day +1
        if int(month) == 0:
            month = 12
            year = int(year) - 1
        if int(month) == 8:
            stop = 1
        day = str(day)
        if len(day) == 1:
            day = '0' + day
        month = str(month)
        if len(month) == 1:
            month = '0' + month
        year = str(year)
    except Exception as err:
        print(err)

json = json.dumps(five_total)
f = open("nba.json","w")
f.write(json)
f.close()
