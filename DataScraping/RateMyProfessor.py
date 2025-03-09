import ratemyprofessor
import json
from Professor import Professor
from Rating import Rating
from Encoder import DateTimeEncoder
from bson.objectid import ObjectId


class RMP:
    def __init__(self):
        self.profNames = []
        self.professors = []
        self.school = ratemyprofessor.get_school_by_name("Drexel University")
        self.ratings = []

    def AddProfessor(self, profName):
        rmpProfessor = ratemyprofessor.get_professor_by_school_and_name(self.school, profName)
        self.professors.append(rmpProfessor)
    
    def GetAllProfessors(self):
        list_of_professors = []
        for current in self.professors:
            ratings = ratemyprofessor.professor.Professor.get_ratings(current)
            for rating in ratings:
                newRatingId = ObjectId()
                rmpRating = Rating(current.id, current.name, rating.difficulty, rating.class_name, rating.date, rating.take_again, rating.grade, rating.online_class, rating.attendance_mandatory, rating.comment)
                self.ratings.append(rmpRating)
            prof = Professor(current.id, current.name, current.rating, current.difficulty)
            list_of_professors.append(prof)
        professor_json = json.dumps([currentprof.__dict__ for currentprof in list_of_professors], indent=4)
        return professor_json

    def GetAllRatings(self):
        return json.dumps([rating.__dict__ for rating in self.ratings], cls=DateTimeEncoder, indent=4)
        
            