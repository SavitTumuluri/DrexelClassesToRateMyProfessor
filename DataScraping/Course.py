class Course:
    def __init__(self):
        self.abbreviation = ""
        self.fullName = ""
        self.prerequisite = ""
        self.creditHours = ""

    def SetName(self, name):
        self.fullName = name

    def SetPrerequisite(self, prereq):
        self.prerequisite = prereq

    def SetAbbr(self, abbr):
        self.abbreviation = abbr
    
    def SetHours(self, credits):
        self.creditHours = credits