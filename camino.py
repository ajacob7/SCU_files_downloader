from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By #used for private xpath call method
from selenium.webdriver.support.ui import Select #used to select a button
from selenium.webdriver.common.keys import Keys #used to select a button
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

import getpass
import time
import sys
import os
import pathlib
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
save_location = pathlib.Path(BASE_DIR + "/SCU")
zipFolder = "course_files_export.zip"

if sys.platform ==  'win32':
	chromedriver_location = os.path.join(BASE_DIR, 'chromedriver')
else:
	chromedriver_location = os.path.join(BASE_DIR, 'mac_chromedriver')

def filesExist(course):
	try:
		driver.find_element_by_class_name('files')
	except NoSuchElementException:
		print("No files tab for " + course + ".")
		return False
	return True



# Setup driver
driver = webdriver.Chrome(chromedriver_location)
username = "ajacob1"

# Login
driver.get("https://camino.instructure.com")
driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
# pw = getpass.getpass()
pw = "Qigz-d4dd-mvli"
driver.find_element_by_xpath('//*[@id="password"]').send_keys(pw + "\n")

# Navigate to courses
driver.find_element_by_xpath('//*[@id="global_nav_courses_link"]').click()
time.sleep(1)
# All courses
driver.find_element_by_xpath('//*[@id="nav-tray-portal"]/span/span/div/div/div/div/ul/li[3]/a').click()
time.sleep(1)

# Get all courses
links = driver.find_element_by_xpath('//*[@id="content"]').find_elements_by_xpath('.//a[@href]')
# Convert courses to list of hrefs
courses = []
for each in links:
	courses.append(each.get_attribute('href'))
	
for course in courses:
	driver.get(course)
	time.sleep(2)
	courseName = driver.find_elements_by_xpath('.//a[@href]')
	courseName = courseName[11].text.split('-')[0]
	print(courseName)
	time.sleep(1)

	#if theres a files section
	if filesExist(courseName):
		os.mkdir(courseName)
		driver.find_element_by_class_name('files').click()
		time.sleep(2)

		# docs = driver.find_elements_by_class_name('al-dropdown__container')
		docs = driver.find_elements_by_class_name('icon-more')

		# driver.find_elements_by_xpath('//*[@id="content"]/div/div[3]/div/div/div/div[5]/div[6]/div[2]/button')
		print("# of docs = ", len(docs))
		for doc in docs:
			doc.click()
			time.sleep(.3)
			dl = driver.find_element_by_link_text('Download')
			
			if "files#" in dl.get_attribute('href'):
				dl.click()
				while(not pathlib.Path(zipFolder).exists()):
					time.sleep(.2)

				with zipfile.ZipFile(currentDir+ "\\" + zipFolder, "r") as zip_ref:
					zip_ref.extractall(currentDir)
				os.remove(zipFolder)



			doc.click()
			# dl.click()
			time.sleep(.3)
	else:
		continue