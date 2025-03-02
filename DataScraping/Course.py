class Course:
    def __init__(self):
        self.prerequisite = ""
        self.abbreviation = ""
        self.creditHours = ""
        self.courseId = ""
        self.fullName = ""

    def SetId(self, courseId):
        self.courseId = courseId

    def SetName(self, name):
        self.fullName = name

    def SetPrerequisite(self, prereq):
        self.prerequisite = prereq

    def SetAbbr(self, abbr):
        self.abbreviation = abbr
    
    def SetHours(self, credits):
        self.creditHours = credits