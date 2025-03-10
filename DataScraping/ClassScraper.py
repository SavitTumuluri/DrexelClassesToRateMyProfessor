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
chrome_driver_path = "chromedriver.exe"

# Initialize the WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(300)


DrexelSignIn.SignIn(driver=driver)
# Navigate to the webpage


driver.get("https://termmasterschedule.drexel.edu/webtms_du/")
time.sleep(5)

fall_quarter_link = driver.find_element(By.LINK_TEXT, "Fall Quarter 24-25")
fall_quarter_link.click()
time.sleep(3)

cci_link = driver.find_element(By.LINK_TEXT, "Col of Computing & Informatics")
cci_link.click()
time.sleep(3)

subjects_table = driver.find_element(By.CSS_SELECTOR, "table.collegePanel")
subject_links = subjects_table.find_elements(By.TAG_NAME, "a")

subjects_data = []
for link in subject_links:
    subject_name = link.text.strip()               # e.g. "Computer Science (CS)"
    subject_href = link.get_attribute("href")      # e.g. /webtms_du/courseList/CS
    if subject_href.startswith("/"):
        # Make it absolute if necessary
        subject_href = "https://termmasterschedule.drexel.edu" + subject_href
    subjects_data.append((subject_name, subject_href))

list_of_professor_names = set()
all_courses = []

for (subj_name, subj_url) in subjects_data:
    print(f"Processing subject: {subj_name} => {subj_url}")
    driver.get(subj_url)
    time.sleep(3)

    # Some subjects may have no courses posted, so wrap in try/except
    try:
        table = driver.find_element(By.ID, "sortableTable")
    except:
        print(f"No table found for subject {subj_name}, skipping.")
        continue

    termMasterInstance = TermMaster.TermMaster(table)
    # Extract JSON if you want to store it by subject
    subject_classes_json = termMasterInstance.ExtractClasses()

    # Collect professor names
    for prof in termMasterInstance.professors:
        list_of_professor_names.add(prof)

    # 6) For each course, get more info from the Catalog
    for courseNumber in termMasterInstance.coursesNumber:
        catalog_url = f"https://catalog.drexel.edu/search/?P={courseNumber}"
        extracted_course = ExtractCourseInfo(driver, catalog_url)
        # If extraction succeeded, store it
        if extracted_course:
            all_courses.append(extracted_course)

# Once all subjects are processed, dump the combined courses to JSON
cs_courses_json = json.dumps([course.__dict__ for course in all_courses], indent=4)
with open("all_computing_informatics_courses.json", "w") as json_file:
    json_file.write(cs_courses_json)

time.sleep(2)

newRMP = RMP()
for professorName in list_of_professor_names:
    currentProfessor = newRMP.AddProfessor(profName=professorName)

professor_json = newRMP.GetAllProfessors()
with open("profesors.json", "w") as json_file:
    json_file.write(professor_json)

time.sleep(6)

ratings_json = newRMP.GetAllRatings()
with open("ratings.json", "w") as json_file:
    json_file.write(ratings_json)

print("sleeping...")
# Close the WebDriver
driver.quit()