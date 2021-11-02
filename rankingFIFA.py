import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import os

print("Opening web browser ")

url = "https://www.fifa.com/fifa-world-ranking/men"
option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)

print("Connecting... ")

driver.get(url)
time.sleep(10)

element = driver.find_element_by_xpath(
    "//div[@class='fc-ranking-overview_cardsContainer__1w_fo']//table")
html_content = element.get_attribute('outerHTML')

print("Done! ")

# Parse HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')


# Structuring content in a Dataframe with Pandas
df_full = pd.read_html(str(table))[0].head(50)
df_part = pd.read_html(str(table))[0].head(10)
df50 = df_full[['RK', 'Team', 'Total PointsPTS', 'Previous Points', '+/-']]
df10 = df_part[['RK', 'Team', 'Total PointsPTS', 'Previous Points', '+/-']]

# Create a dictionary with the collected data
top10FIFA = {}
top50FIFA = {}
top10FIFA['ranking'] = df10.to_dict('records')
top50FIFA['ranking'] = df50.to_dict('records')

# Convert and save file in JSON format
top = json.dumps(top50FIFA)
fp = open('top50FIFA.json', 'w')
fp.write(top)

top = json.dumps(top10FIFA)
fp = open('top10FIFA.json', 'w')
fp.write(top)

fp.close()

print("top50FIFA.json and top10FIFA.json were created \n")

print("Closing web browser ")
driver.quit()

os.system('clear')  # Clean console in Linux
os.system('CLS')  # Clean console in Windows

print("\n Top 10 -- Ranking FIFA")
print(df10)
print("\n Top 50 -- Ranking FIFA")
print(df50)
