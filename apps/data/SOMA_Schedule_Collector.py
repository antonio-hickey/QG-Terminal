#--------------------------------------------------------------------------------------------------------
# Importing Python Modules
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime as dt
import csv
import time
import pandas as pd
#--------------------------------------------------------------------------------------------------------
# Browser Path
PATH = "/home/sratus/Desktop/API/chromedriver"
options = webdriver.ChromeOptions()
options.binary_location = '/usr/bin/google-chrome'
prefs = {'download.default_directory' : "/home/sratus/QG Terminal/QGTerminal/apps/data/"}
options.add_experimental_option('prefs',prefs)
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
#--------------------------------------------------------------------------------------------------------
# Request Page
driver.get('https://www.newyorkfed.org/markets/domestic-market-operations/monetary-policy-implementation/treasury-securities/treasury-securities-operational-details#current-schedule')
#--------------------------------------------------------------------------------------------------------
# Target Data
n_rows = driver.find_elements_by_xpath("/html/body/div[1]/div[3]/div[2]/div[2]/div[1]/div/div[2]/div/table/tbody/tr")
n_rows = len(n_rows)
#--------------------------------------------------------------------------------------------------------
# Rows
r = []
for row in range(n_rows):
    c1 = driver.find_element_by_css_selector("#current-schedule-table > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(1)".format(row + 1))
    c1 = c1.text
    c2 = driver.find_element_by_css_selector("#current-schedule-table > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(5)".format(row + 1))
    c2 = c2.text
    c2 = c2.replace('\n',' ')
    c3 = driver.find_element_by_css_selector("#current-schedule-table > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(7)".format(row + 1))
    c3 = c3.text
    r.append([c1,c2,c3])
#--------------------------------------------------------------------------------------------------------
# Columns
columns = ["Operation Date","Security","Max Purchase Size"]
#--------------------------------------------------------------------------------------------------------
# Export Dataset
filename = "schedule.csv" # Export As
with open(filename,'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(columns)
    for row in r:
        csvwriter.writerow(row)
#--------------------------------------------------------------------------------------------------------
