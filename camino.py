import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By #used for private xpath call method
from selenium.webdriver.support.ui import Select #used to select a button
from selenium.webdriver.common.keys import Keys #used to select a button
from selenium.webdriver.chrome.options import Options #used for headless browser function
import getpass
import time
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if sys.platform ==  'win32':
	chromedriver_location = os.path.join(BASE_DIR, 'chromedriver')
else:
	chromedriver_location = os.path.join(BASE_DIR, 'mac_chromedriver')
#Setup driver
driver = webdriver.Chrome(chromedriver_location)
# driver = webdriver.Chrome()
username = "ajacob1"

#Login
driver.get("https://camino.instructure.com")
driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
pw = getpass.getpass()
driver.find_element_by_xpath('//*[@id="password"]').send_keys(pw + "\n")

#Navigate to courses
driver.find_element_by_xpath('//*[@id="global_nav_courses_link"]').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="nav-tray-portal"]/span/span/div/div/div/div/ul/li[3]/a').click()

time.sleep(1)
courses = driver.find_elements_by_xpath("//a[@href]")

for course in courses:
	print(course)
	#navigate to courses
	# if :#exists file subsection
	# 	#navigate to files
	# 	for file in files:
			
	# else:
	# 	continue





# currentFolder
# os.rename("C:/Users/asaja/Downloads/"+currentFile, currentFolder + "/" + currentFile)