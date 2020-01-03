import requests
from bs4 import BeautifulSoup
import re


page = requests.get("https://projects.fivethirtyeight.com/2018-nba-predictions/games/?ex_cid=rrpromo")

print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())
games = {}
teams = {}
scores = {}
i=30
while (i<60):
    a = soup.find_all('tbody', class_='ie10up')[i].get_text()
    #accomodate 76ers because numbers in name
    pattern = re.compile(r'[a-z,7,6]{4,}', re.IGNORECASE)
    pattern2 = re.compile(r'..(?=%)')
    result = pattern.findall(a)
    result2 = pattern2.findall(a)
    #accomodate Trail Blazers because two words
    if len(result)>2:
        if result[0] == 'Trail':
            teams[i] = ['Trail Blazers', result[2]]
        else:
            teams[i] = [result[0], 'Trail Blazers']
    else:
        teams[i] = result
    scores[i] = result2
    i +=1

games = teams, scores
print(games)


for game in games[0]:
    print("----game----")
    print(games[0][game][0], "vs", games[0][game][1])


# i=0
# while (i<200):
#     if (int(games[1][i][0]) > 69):
#         print(games[0][i][0])
#     elif (int(games[1][i][1]) > 69):
#         print(games[0][i][1])
#     i+=1


page = requests.get("http://www.donbest.com/nba/odds/money-lines/20180101.html")
print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')
name_box = soup.findAll('span', attrs={'oddsTeamWLink'})

print(name_box)

for team in name_box:
    print(team)
