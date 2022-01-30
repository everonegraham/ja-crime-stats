import json
from requests import get
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

URL = "https://jcf.gov.jm/stats/"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(60)

driver.get(URL)

soup = BeautifulSoup(driver.page_source, "html.parser")
crime_table = soup.find("table", {"class": "google-visualization-table-table"})

table_data = crime_table.find_all("tr")
table_headers = table_data[0].find_all("th")

table_rows = table_data[1:]
table_data_list = []

for row in table_rows:

    row_data = []
    for cell in row.find_all("td"):
        row_data.append(cell.text)

    table_data_list.append(row_data)

table_headers_list = []

for header in table_headers:
    table_headers_list.append(header.text)

table_data_dict = {}
for row in table_data_list:
    
    row_data_dict = {}
    for i in range(len(row)):
        
        row_data_dict[table_headers_list[i]] = row[i]
    
    table_data_dict[row[0]] = row_data_dict

#print(table_data_dict)
print("Writing to file...")

with open("crime-data.json", "w") as f:
    json.dump(table_data_dict, f)

driver.quit()
