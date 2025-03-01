from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def extractClasses(table):
    # Extract table headers
    headers = []
    header_row = table.find_element(By.TAG_NAME, "thead")
    header_cells = header_row.find_elements(By.TAG_NAME, "th")
    for header in header_cells:
        headers.append(header.text.strip())

    # Extract table rows
    rows = []
    table_body = table.find_element(By.TAG_NAME, "tbody")
    table_rows = table_body.find_elements(By.TAG_NAME, "tr")

    for row in table_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells:
            row_data = [cell.text.strip() for cell in cells]
            rows.append(row_data)
    return rows
# Print or process the data
    '''
    print("Headers:", headers)
    for row in rows:
        print(row)
        '''
    

