from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import time
import Class

class TermMaster:
    def __init__(self, importTable):
        self.table = importTable
        self.coursesNumber = None
        self.professors = None

    

    def ExtractClasses(self):
        # Extract table headers
        headers = []
        header_row = self.table.find_element(By.TAG_NAME, "thead")
        header_cells = header_row.find_elements(By.TAG_NAME, "th")
        for header in header_cells:
            headers.append(header.text.strip())

        # Extract table rows
        rows = []
        table_body = self.table.find_element(By.TAG_NAME, "tbody")
        table_rows = table_body.find_elements(By.TAG_NAME, "tr")

        for row in table_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:
                row_data = [cell.text.strip() for cell in cells]
                if len(row_data) > 5:
                    rows.append(row_data)
        self.SetClassesModel(rows)
        self.ExtractProfessors(rows)

    def SetClassesModel(self, classes):
        list_of_classes = []
        list_of_courseNumber = set()
        for current in classes:
            subjectCode = current[0] + " " + current[1]
            list_of_courseNumber.add(subjectCode)
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

        self.coursesNumber = list_of_courseNumber
        json_data = json.dumps([eachClass.__dict__ for eachClass in list_of_classes], indent=4)
        return json_data

    def ExtractProfessors(self, rows):
        list_of_professors = set()
        for currentClass in rows:
            possibleProfessor = currentClass[10]
            if (possibleProfessor != None or possibleProfessor.lower() != "tbd"):
                list_of_professors.add(possibleProfessor)
        
        self.professors = list_of_professors
        
    
