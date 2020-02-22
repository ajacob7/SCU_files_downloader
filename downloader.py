from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import getpass
import time
import sys
import os
import pathlib
import zipfile
import shutil
import re

docCount = 0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
save_location = pathlib.Path(BASE_DIR + "/SCU")
zipFolder = "course_files_export.zip"
Downloads = pathlib.Path("C:/Users/Asa/Downloads")

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

def elementNewTab(element):
	ActionChains(driver) \
			    .key_down(Keys.CONTROL) \
			    .click(element) \
			    .key_up(Keys.CONTROL) \
			    .perform()

def uniqueFolder(folderPath):
	copyVal = 0
	tempFolder = folderPath
	while True:
		if not pathlib.Path(tempFolder).exists():
			return pathlib.Path(tempFolder)
		copyVal += 1
		tempFolder = folderPath + "(" + str(copyVal) + ")"

def iterDocs(path, folder, level):
	global docCount
	# print("Making directory:" + folder)
	folder = re.sub(r'[\\/\:*"<>\|\.%\$\^&£]', '-', folder)
	newPath =  pathlib.Path(path).joinpath(folder)

	# print("Changing download location to: ", newPath, "\n")
	# os.mkdir() #make a folder for the course

	rows = driver.find_elements_by_class_name('ef-item-row')
	docs = driver.find_elements_by_class_name('icon-more')

	if(len(rows) > 0):
		newPath = uniqueFolder(str(newPath))
		os.mkdir(newPath)
	else:
		return

	print("Creating folder:", newPath)
	for row, doc in zip(rows, docs):
		icon = row.find_element_by_xpath(".//i")
		rowText = row.find_element_by_class_name("ef-name-col__text")
		itemName = rowText.text
		itemName = re.sub(r'[\\/\:*"<>\|%\^]', '_', itemName)
		if ("media-object ef-big-icon FilesystemObjectThumbnail mimeClass-folder" in icon.get_attribute("class")):
			elementNewTab(rowText)
			# time.sleep(.4)
			driver.switch_to.window(driver.window_handles[-1])
			# time.sleep(.4)
			iterDocs(newPath, itemName, level + 1)
			driver.close()
			driver.switch_to.window(driver.window_handles[level])
			# print("reverting download to: ", newPath)
		else:
			doc.click()
			docCount = docCount + 1
			time.sleep(.1)
			download = driver.find_element_by_link_text('Download')
			download.click()
			counter = 0
			while(not pathlib.Path(Downloads).joinpath(itemName).resolve().exists()):
				if(counter % 5 == 0):
					print("Waiting on ", pathlib.Path(Downloads).joinpath(itemName))
				time.sleep(.1)
				counter += 1
			downloadPath = pathlib.Path(Downloads).joinpath(itemName)
			shutil.move(str(downloadPath), str(newPath))
			webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


# Setup driver
driver = webdriver.Chrome(chromedriver_location)
options = webdriver.ChromeOptions()
username = input("Enter username for camino.instructure.com:")
pw = getpass.getpass()

# Login
driver.get("https://camino.instructure.com")
driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)

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

skip = 0
courseNo = 0
for course in courses:
	courseNo += 1
	if skip != 0:
		skip -= 1 
		continue
	driver.get(course)
	time.sleep(.2)
	courseName = driver.find_elements_by_xpath('.//a[@href]')[11].text.split('-')[0]
	print(courseName, courseNo)
	time.sleep(1)

	if filesExist(courseName):
		driver.find_element_by_class_name('files').click()
		time.sleep(2)
		iterDocs(save_location, courseName, 0)
	else:
		continue
print(docCount, "documents downloaded")
