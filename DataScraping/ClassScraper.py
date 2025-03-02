from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import Course
import json
import RateMyProfessor
import DrexelSignIn
import Class
import TermMaster

# Set up Chrome options (optional)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")


def ExtractCourseInfo(driver, url):
    try:
        driver.get(url)
        time.sleep(2)
        searchbox = driver.find_element(By.ID, "fssearchresults")
        courseHead = searchbox.find_element(By.TAG_NAME, "h2")
        courseInfo = courseHead.text.strip()
        time.sleep(2)
        return ParseCourseInfo(searchbox.get_attribute('innerHTML'))
    except TimeoutException:
        print("Page load timed out. Trying again...")
        driver.refresh()  # Try reloading the page
    

def ParseCourseInfo(courseInfo):
    soup = BeautifulSoup(courseInfo, "html.parser")

    # Extract Course Title
    course_title = soup.find("h2").text.strip()
    match = re.match(r"(\w+)\s*(\d+)\s*(.+)\s*(\d+\.\d+)\s*Credits", course_title)
    newCourse = Course.Course()
    if match:
        newCourse.SetAbbr(match.group(1) + match.group(2)) # CS
        #course_number = match.group(2)  # 260
        newCourse.SetName(match.group(3).strip())  # Data Structures
        newCourse.SetHours(match.group(4))  # 4.0

    # Extract Restrictions
    prerequisites = None
    for b_tag in soup.find_all("b"):
        if "Prerequisites" in b_tag.text:
            prerequisites = b_tag.next_sibling.strip()
    newCourse.SetPrerequisite(prerequisites)
    return newCourse
    


# Path to your ChromeDriver
chrome_driver_path = "C:/Users/Serena Osuagwu/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# Initialize the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(300)


DrexelSignIn.SignIn(driver=driver)
# Navigate to the webpage
termMaster = "https://termmasterschedule.drexel.edu/webtms_du/courseList/CS"  # Replace with the actual URL
driver.get(termMaster)

# Wait for the page to load (adjust the sleep time as needed)
time.sleep(5)

# Locate the table by its ID
table = driver.find_element(By.ID, "sortableTable")

termMasterInstance = TermMaster.TermMaster(table)
classes_json = termMasterInstance.ExtractClasses()
allCourses = []
for courseNumber in termMasterInstance.coursesNumber:
    catalogurl = f"https://catalog.drexel.edu/search/?P={courseNumber}"
    course = ExtractCourseInfo(driver=driver, url=catalogurl)
    allCourses.append(course)
courses_json = json.dumps([course.__dict__ for course in allCourses], indent=4)
list_of_professors = []
for professor in termMasterInstance.professors:
    currentProfessor = RateMyProfessor.GetProfessors(professor)
    if (currentProfessor):
        list_of_professors.append(currentProfessor)

professor_json = json.dumps([prof.__dict__ for prof in list_of_professors], indent=4)
print(professor_json)

'''professor_json = RateMyProfessor.GetProfessors()
print(professor_json)'''


# Close the WebDriver
driver.quit()