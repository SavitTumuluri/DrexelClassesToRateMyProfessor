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
from RateMyProfessor import RMP
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


cs_page = "https://termmasterschedule.drexel.edu/webtms_du/courseList/CS"  # Replace with the actual URL
driver.get(cs_page)

# Wait for the page to load (adjust the sleep time as needed)
time.sleep(5)

list_of_professor_names = []

# Locate the table by its ID
table = driver.find_element(By.ID, "sortableTable")

termMasterInstance = TermMaster.TermMaster(table)
cs_classes_json = termMasterInstance.ExtractClasses()
with open("cs_classes.json", "w") as json_file:
    json_file.write(cs_classes_json)

print(cs_classes_json)
time.sleep(2)

list_of_professor_names.extend(termMasterInstance.professors)

allCourses = []
for courseNumber in termMasterInstance.coursesNumber:
    catalogurl = f"https://catalog.drexel.edu/search/?P={courseNumber}"
    course = ExtractCourseInfo(driver=driver, url=catalogurl)
    allCourses.append(course)
cs_courses_json = json.dumps([course.__dict__ for course in allCourses], indent=4)
print(cs_courses_json)
with open("cs_courses.json", "w") as json_file:
    json_file.write(cs_courses_json)

time.sleep(2)

'''professor_json = RateMyProfessor.GetProfessors()
print(professor_json)'''

se_page = "https://termmasterschedule.drexel.edu/webtms_du/courseList/SE"  # Replace with the actual URL
driver.get(se_page)

# Wait for the page to load (adjust the sleep time as needed)
time.sleep(5)

# Locate the table by its ID
se_table = driver.find_element(By.ID, "sortableTable")

secondTermMasterInstance = TermMaster.TermMaster(se_table)
se_classes_json = secondTermMasterInstance.ExtractClasses()
print(se_classes_json)
with open("se_classes.json", "w") as json_file:
    json_file.write(se_classes_json)

time.sleep(2)
list_of_professor_names.extend(secondTermMasterInstance.professors)

seCourses = []
for courseNumber in secondTermMasterInstance.coursesNumber:
    catalogurl = f"https://catalog.drexel.edu/search/?P={courseNumber}"
    newCourse = ExtractCourseInfo(driver=driver, url=catalogurl)
    seCourses.append(newCourse)
se_courses_json = json.dumps([course.__dict__ for course in seCourses], indent=4)
print(se_courses_json)
with open("se_courses.json", "w") as json_file:
    json_file.write(se_courses_json)

print("sleeping...")
time.sleep(4)

'''newRMP = RMP()
for professorName in list_of_professor_names:
    print(professorName)
    currentProfessor = newRMP.AddProfessor(profName=professorName)

professor_json = newRMP.GetAllProfessors()
print(professor_json)'''

# Close the WebDriver
driver.quit()