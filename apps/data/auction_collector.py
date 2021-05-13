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
import os
import time
import pandas as pd
#--------------------------------------------------------------------------------------------------------
# Browser Path
PATH = "/home/sratus/Desktop/API/chromedriver"
options = webdriver.ChromeOptions()
options.binary_location = '/usr/bin/google-chrome'
prefs = {'download.default_directory' : "/home/sratus/QG Terminal/QG-Terminal/apps/data/"}
options.add_experimental_option('prefs',prefs)
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
#--------------------------------------------------------------------------------------------------------
# Request Page
driver.get('https://www.treasurydirect.gov/instit/instit.htm?upcoming')
time.sleep(3) # wait 3 seconds
#--------------------------------------------------------------------------------------------------------
# Define Target Data

# Bills Table
bills_n_rows = driver.find_elements_by_xpath("/html/body/div[1]/div/section/div/div[2]/table[1]/tbody/tr")
bills_n_rows = len(bills_n_rows)
bills_r = []
if bills_n_rows > 1:
    for j in range(bills_n_rows):
        maturity = driver.find_element_by_css_selector("#institTableBillsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(1)".format(j + 1))  
        cusip = driver.find_element_by_css_selector("#institTableBillsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(3)".format(j + 1))
        amount = driver.find_element_by_css_selector("#institTableBillsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(4)".format(j + 1))
        date = driver.find_element_by_css_selector("#institTableBillsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(6)".format(j + 1))
        bills_r.append([maturity.text,cusip.text,amount.text,date.text])

# Notes Table
notes_n_rows = driver.find_elements_by_xpath("/html/body/div[1]/div/section/div/div[2]/table[2]/tbody/tr")
notes_n_rows = len(notes_n_rows)
notes_r = []
if notes_n_rows > 1:
    for j in range(notes_n_rows):
        maturity = driver.find_element_by_css_selector("#institTableNotesUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(1)".format(j+ 1))
        cusip = driver.find_element_by_css_selector("#institTableNotesUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(3)".format(j + 1))
        amount = driver.find_element_by_css_selector("#institTableNotesUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(4)".format(j + 1))
        date = driver.find_element_by_css_selector("#institTableNotesUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(6)".format(j + 1))
        notes_r.append([maturity.text,cusip.text,amount.text,date.text])

# Bonds Table
bonds_n_rows = driver.find_elements_by_xpath("/html/body/div[1]/div/section/div/div[2]/table[3]/tbody/tr")
bonds_n_rows = driver.find_elements_by_xpath("/html/body/div[1]/div/section/div/div[2]/table[2]/tbody/tr")
bonds_n_rows = len(bonds_n_rows)
bonds_r = []
if bonds_n_rows > 1:
    for j in range(bonds_n_rows):
        maturity = driver.find_element_by_css_selector("#institTableBondsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(1)".format(j+ 1))
        cusip = driver.find_element_by_css_selector("#institTableBondsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(3)".format(j + 1))
        amount = driver.find_element_by_css_selector("#institTableBondsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(4)".format(j + 1))
        date = driver.find_element_by_css_selector("#institTableBondsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(6)".format(j + 1))
        bonds_r.append([maturity.text,cusip.text,amount.text,date.text])

# TIPS Table
tips_n_rows = driver.find_elements_by_xpath("/html/body/div[1]/div/section/div/div[2]/table[4]/tbody/tr")
tips_n_rows = driver.find_elements_by_xpath("/html/body/div[1]/div/section/div/div[2]/table[2]/tbody/tr")
tips_n_rows = len(tips_n_rows)
tips_r = []
if tips_n_rows > 1:
    for j in range(tips_n_rows):
        maturity = driver.find_element_by_css_selector("#institTableTipsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(1)".format(j+ 1))
        cusip = driver.find_element_by_css_selector("#institTableTipsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(3)".format(j + 1))
        amount = driver.find_element_by_css_selector("#institTableTipsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(4)".format(j + 1))
        date = driver.find_element_by_css_selector("#institTableTipsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(6)".format(j + 1))
        tips_r.append([maturity.text,cusip.text,amount.text,date.text])

# FRNs Table 
frn_n_rows = driver.find_elements_by_xpath("/html/body/div[1]/div/section/div/div[2]/table[5]/tbody/tr")
frn_n_rows = driver.find_elements_by_xpath("/html/body/div[1]/div/section/div/div[2]/table[2]/tbody/tr")
frn_n_rows = len(frn_n_rows)
frn_r = []
if frn_n_rows > 1:
    for j in range(frn_n_rows):
        maturity = driver.find_element_by_css_selector("#institTableFrnsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(1)".format(j+ 1))
        cusip = driver.find_element_by_css_selector("#institTableFrnsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(3)".format(j + 1))
        amount = driver.find_element_by_css_selector("#institTableFrnsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(4)".format(j + 1))
        date = driver.find_element_by_css_selector("#institTableFrnsUpcoming > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(6)".format(j + 1))
        frn_r.append([maturity.text,cusip.text,amount.text,date.text])

# Export data to csv
columns = ["Maturity","CUISP","Amount","Date"]
os.chdir(os.path.dirname(__file__))
filename = "auction_schedule.csv"
with open(filename,'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(columns)
    for row in bills_r:
        csvwriter.writerow(row)
    for row in notes_r:
        csvwriter.writerow(row)
    for row in bonds_r:
        csvwriter.writerow(row)
    for row in tips_r:
        csvwriter.writerow(row)
    for row in frn_r:
        csvwriter.writerow(row)

#--------------------------------------------------------------------------------------------------------
# Close Driver
driver.quit()
#--------------------------------------------------------------------------------------------------------
