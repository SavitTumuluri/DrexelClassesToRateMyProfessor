class Rating:
    def __init__(self, profId, profname, difficulty, rateClass, date, take_again, grade, online_class, attendance_mandatory, comment):
        self.profId = profId
        self.profName = profname
        self.difficulty = difficulty
        self.class_name = rateClass
        self.date = date
        self.take_again = take_again
        self.grade = grade
        self.online_class = online_class
        self.attendance_mandatory = attendance_mandatory
        self.comment = comment

    
    def SetMetadata(self, metadata):
        self.metadata = metadata

    def SetComment(self, comment):
        self.comment = comment