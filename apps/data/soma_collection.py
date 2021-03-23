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
driver.get('https://www.newyorkfed.org/markets/soma-holdings#export-builder')

# Define Target Data
time.sleep(5) # Wait 5 seconds
t_bills = driver.find_element_by_css_selector("tr.ng-star-inserted:nth-child(1) > td:nth-child(2)")
t_nb = driver.find_element_by_css_selector("tr.ng-star-inserted:nth-child(2) > td:nth-child(2)")
t_frn = driver.find_element_by_css_selector("tr.ng-star-inserted:nth-child(3) > td:nth-child(2)")
t_tips = driver.find_element_by_css_selector("tr.ng-star-inserted:nth-child(4) > td:nth-child(2)")
t_FAS = driver.find_element_by_css_selector("tr.ng-star-inserted:nth-child(5) > td:nth-child(2)")
t_AMBS = driver.find_element_by_css_selector("tr.ng-star-inserted:nth-child(6) > td:nth-child(2)")
t_CMBS = driver.find_element_by_css_selector("tr.ng-star-inserted:nth-child(7) > td:nth-child(2)")
soma = driver.find_element_by_css_selector("tr.ng-star-inserted:nth-child(8) > td:nth-child(2)")
change = driver.find_element_by_css_selector("tr.ng-star-inserted:nth-child(9) > td:nth-child(2)")

# Export data to csv
filename = "SOMA.csv"
date = dt.today().strftime('%Y-%m-%d')
t_bills_r = [date,"T-Bills",t_bills.text]
t_nb_r = [date,"T-Notes & T-Bonds",t_nb.text]
t_frn_r = [date,"Floating Rate Notes",t_frn.text]
t_tips_r = [date,"TIPS",t_tips.text]
t_FAS_r = [date,"FAS",t_FAS.text]
t_AMBS_r = [date,"AMBS",t_AMBS.text]
t_CMBS_r = [date,"CMBS",t_CMBS.text]
soma_r = [date,"Total",soma.text]
change_r = [date,"Change",change.text]
columns = ["Date","Security","Value"]
rows = [t_bills_r, t_nb_r,t_frn_r,t_tips_r,t_FAS_r,t_AMBS_r,t_CMBS_r,soma_r,change_r]

# Most recent
with open(filename,'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(columns)
    for row in rows:
        csvwriter.writerow(row)

# Historical Dataset
filename_hist = "SOMA_hist.csv" 
row_hist = [date,t_bills.text,t_nb.text,t_frn.text,t_tips.text,t_FAS.text,t_AMBS.text,t_CMBS.text,soma.text,change.text]

with open(filename_hist,'a') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(row_hist)
#--------------------------------------------------------------------------------------------------------
# Close Driver
driver.quit()
#--------------------------------------------------------------------------------------------------------
