from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
import pandas as pd
from fake_useragent import UserAgent
from time import sleep
from random import randint
from selenium import webdriver
import sys
import datetime
import time
from datetime import timedelta, date
import os
#from itertools import zip_longest
#from selenium.webdriver.common.action_chains import ActionChains
#import requests

query_freq_in_mins = 6
class my_dictionary(dict):  

	# __init__ function  
	def __init__(self):  
		self = dict()  

	# Function to add key:value  
	def add(self, key, value):  
		self[key] = value  

jobs_how_long_ago = my_dictionary()

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
#options.add_argument('--incognito')
#options.add_argument('--headless')

upwork_username = 'geldabhojal'
upwork_password = 'Bgt56yhN_'

# Upwork Login
driver = webdriver.Chrome("/Users/khugel01/Downloads/chromedriver", options=options)
driver.get("https://www.upwork.com/ab/account-security/login")
driver.find_elements_by_xpath("//input[@id='login_username']")[0].send_keys(upwork_username)
driver.find_elements_by_xpath("//button[@id='login_password_continue']")[0].click()
sleep(6)
driver.find_elements_by_xpath("//input[@id='login_password']")[0].send_keys(upwork_password)
driver.find_elements_by_xpath("//button[@id='login_control_continue']")[0].click()
sleep(6)

# Go to search Page in Upworks
driver.get("https://www.upwork.com/ab/jobs/search/")
sleep(8)
driver.maximize_window()

## Tries to click on drop down list - Unsuccessful
#driver.find_elements_by_xpath("//input[@placeholder='Select Categories' and @class='up-input']")[0].click()
# element = driver.find_elements_by_xpath("//input[@id=531770282593251331]")[0]
# actions = ActionChains(driver)
# actions.move_to_element(element).perform()
#driver.find_elements_by_xpath("//input[@id=531770282593251331]")[0].click()

# Search every saved search at regular intervals
while(True):
	# Click on Search box
	driver.find_elements_by_xpath("//input[@type='search' and @id='search-box-el']")[0].click()
	sleep(2)
	# Get number of saved searches
	saved_searches = len(driver.find_elements_by_xpath("//span[contains(@class,'saved-search-suggestion-label')]"))
	for x in range(saved_searches):
		driver.find_elements_by_xpath("//input[@type='search' and @id='search-box-el']")[0].click()
		sleep(2)
		saved_searches = driver.find_elements_by_xpath("//span[contains(@class,'saved-search-suggestion-label')]")
		sleep(2)
		print('Searching for latest jobs for {} at {}'.format(saved_searches[x].text, datetime.datetime.now().time()))
		saved_searches[x].click()
		sleep(5)
		page_source = driver.page_source
		page_soup = soup(page_source, "html.parser")
		#print(page_soup.prettify())
		all_jobs = page_soup.findAll("div", {"data-job-tile": "::job"})
		for job in all_jobs:
			jobs_how_long_ago[job.div.div.div.h4.a.text] = ['https://www.upwork.com'+job.div.div.div.h4.a['href'], job.div.div.div.div.small.findAll("span")[9].time.text]

		print("{:<100} {:<100}".format('==========', '==========')) 
		print("{:<100} {:<100} {:<100}".format('JOB', 'Link', 'Posted')) 
		for key, value in jobs_how_long_ago.items(): 
			job_summary = key
			job_link = value[0]
			posted = value[1]
			print("{:<100} {:<100} {:<100}".format(job_summary, job_link, posted))
	time.sleep(query_freq_in_mins*60)

driver.close()

# Pop-up notification in MAC
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

notify("Title", "Heres an alert")

