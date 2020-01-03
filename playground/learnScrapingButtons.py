from selenium import webdriver
import time
from bs4 import BeautifulSoup


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
print(soup)
