import re
transcript = '''
Fall Quarter 22-23
Course
Title
Grade
Credits


BIO 132
Genetics and Evolution
T
4




Satisfied by: AP20 - AP Biology - College Board AP Credit
CI 101
Comp & Info Design I
A
2


CIVC 101
Intro to Civic Engagement
B+
1


CS 164
Intro to Computer Science
A-
3


ECON 202
Principles of Macroeconomics
T
4




Satisfied by: AP35 - AP Economics: Macroeconomics - College Board AP Credit
ENGL 101
Composition and Rhetoric I
T
3




Satisfied by: AP36 - AP English Language & Comp - College Board AP Credit
ENTP 100
Innovation Ecosystem
A+
1


MATH 121
Calculus I
T
4




Satisfied by: AP68 - AP Calculus BC - College Board AP Credit
MATH 122
Calculus II
T
4




Satisfied by: AP68 - AP Calculus BC - College Board AP Credit
MATH 123
Calculus III
D
4


PSY 101
General Psychology I
C-
3


UNIV CI101
The Drexel Experience
C
1
'''

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

if __name__ == '__main__':
    message = parse_transcipts(transcript)
    print(message)

