import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

print("Opening web browser ")

url = "https://www.fifa.com/fifa-world-ranking/men"
option = Options()
option.headless = True
driver = webdriver.Firefox(options = option)

print("Connecting... ")

driver.get(url)
time.sleep(10)

element = driver.find_element_by_xpath("//div[@class='fc-ranking-overview_cardsContainer__1w_fo']//table")
html_content = element.get_attribute('outerHTML')

print("Done! ")

# Parse HTML content with BeautifulSoup 
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name = 'table')


# Structuring content in a Dataframe with Pandas 
df_full = pd.read_html(str(table))[0].head(10)
df = df_full[['RK', 'Team', 'Total PointsPTS', 'Previous Points', '+/-']]
print(df)

# Create a dictionary with the collected data 
top10FIFA = {}
top10FIFA['ranking'] = df.to_dict('records')

# Convert and save file in JSON format 
json = json.dumps(top10FIFA)
fp = open('ranking.json', 'w')
fp.write(json)
fp.close()

print("ranking.json was created \n")

driver.quit()