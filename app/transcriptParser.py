import re

def is_class_passed(grade):
    invalidGrades = ["C-", "D+", "D", "D-", "F", "W", "NF"]
    if grade in invalidGrades:
        return False
    
    return True

def parse_transcipts(transcript):
    pattern = r'([A-Za-z]+\s\d{3})\s+.*\s+([A-Za-z\+-]+)\s+[\d\.]+'
    necessaryInfo = re.findall(pattern, transcript)
    completedCourse = []
    for i in necessaryInfo:
        course, grade = i
        if is_class_passed(grade):
            completedCourse.append(course)
    return completedCourse


