from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import DrexelSignIn
import TermMaster

# Set up Chrome options (optional)
chrome_options = Options()


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





# Close the WebDriver
driver.quit()