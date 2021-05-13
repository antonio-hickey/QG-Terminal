#--------------------------------------------------------------------------------------------------------
# Importing Python Modules
#--------------------------------------------------------------------------------------------------------
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import ast
import sys
from sys import argv, exit
import time
import csv
import os
import datetime as dt
import pandas as pd
import numpy as np
from math import sqrt, pi, log, e
from enum import Enum
import scipy.stats as stat
from scipy.stats import norm
from scipy import stats
import sympy
from sympy.stats import Normal, cdf
from sympy import init_printing
init_printing()
#--------------------------------------------------------------------------------------------------------
# Browser Path
#--------------------------------------------------------------------------------------------------------
PATH = "/home/sratus/Desktop/API/chromedriver"
options = webdriver.ChromeOptions()
options.binary_location = '/usr/bin/google-chrome'
options.add_argument('headless')
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(ChromeDriverManager().install())
#--------------------------------------------------------------------------------------------------------
# Function
#--------------------------------------------------------------------------------------------------------
def bot():
    #   Go to cnbc.com
    driver.get('https://www.cnbc.com/us-treasurys/')
    time.sleep(5)                             
    mo1 = driver.find_element_by_css_selector('.BasicTable-tableBody > tr:nth-child(1) > td:nth-child(2)')
    mo1 = mo1.text
    mo3 = driver.find_element_by_css_selector('.BasicTable-tableBody > tr:nth-child(2) > td:nth-child(2)')
    mo3 = mo3.text
    mo6 = driver.find_element_by_css_selector('.BasicTable-tableBody > tr:nth-child(3) > td:nth-child(2)') 
    mo6 = mo6.text
    yr1 = driver.find_element_by_css_selector('.BasicTable-tableBody > tr:nth-child(4) > td:nth-child(2)')
    yr1 = yr1.text
    yr2 = driver.find_element_by_css_selector('.BasicTable-tableBody > tr:nth-child(5) > td:nth-child(2)')
    yr2 = yr2.text
    yr3 = driver.find_element_by_css_selector('.BasicTable-tableBody > tr:nth-child(6) > td:nth-child(2)') 
    yr3 = yr3.text
    yr5 = driver.find_element_by_css_selector('.BasicTable-tableBody > tr:nth-child(7) > td:nth-child(2)') 
    yr5 = yr5.text
    yr7 = driver.find_element_by_css_selector('.BasicTable-tableBody > tr:nth-child(8) > td:nth-child(2)')
    yr7 = yr7.text
    yr10 = driver.find_element_by_css_selector('.BasicTable-tableBody > tr:nth-child(9) > td:nth-child(2)')
    yr10 = yr10.text
    yr20 = driver.find_element_by_css_selector('.BasicTable-tableBody > tr:nth-child(10) > td:nth-child(2)')
    yr20 = yr20.text
    yr30 = driver.find_element_by_css_selector('.BasicTable-tableBody > tr:nth-child(11) > td:nth-child(2)')
    yr30 = yr30.text

    # Data
    date = (dt.datetime.now().strftime("%Y-%m-%d")) 
    row = [date,mo1,mo3,mo6,yr1,yr2,yr3,yr5,yr7,yr10,yr20,yr30]

    # Write dataset
    os.chdir(os.path.dirname(__file__))
    filename = ('USTCurve.csv')
    with open(filename,'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row)
    driver.quit()
#--------------------------------------------------------------------------------------------------------
# Calling Function
bot()
#--------------------------------------------------------------------------------------------------------
