from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import DrexelSignIn
import Class
import TermMaster

# Set up Chrome options (optional)
chrome_options = Options()

list_of_classes = []

# Path to your ChromeDriver
chrome_driver_path = "C:/Users/Serena Osuagwu/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# Initialize the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


DrexelSignIn.SignIn(driver=driver)
# Navigate to the webpage
termMaster = "https://termmasterschedule.drexel.edu/webtms_du/courseList/CS"  # Replace with the actual URL
driver.get(termMaster)

# Wait for the page to load (adjust the sleep time as needed)
time.sleep(5)

# Locate the table by its ID
table = driver.find_element(By.ID, "sortableTable")

classes = TermMaster.extractClasses(table=table)

for current in classes:
    subjectCode = current[0] + current[1]
    classType = current[2]
    method = current[3]
    section = current[4]
    crn = current[5]
    name = current[6]
    splitDate = current[7].split(" ", 1)
    
    if (len(splitDate) > 1):
        date = splitDate[0]
        timesplit = splitDate[1].split('\n')
        classTime = timesplit[0]
    else :
        date = splitDate[0]
        classTime = splitDate[0]
    professor = current[8]
    newClass = Class.Class(subjectCode=subjectCode, classType=classType, method=method, section=section, crn=crn, name=name, date=date, classTime=classTime, professor=professor)
    list_of_classes.append(newClass)



# Close the WebDriver
driver.quit()