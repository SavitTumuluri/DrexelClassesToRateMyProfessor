import ratemyprofessor
import json
import Professor
from Encoder import DateTimeEncoder
from datetime import datetime

class RMP:
    def __init__(self):
        self.professors = []
        self.school = ratemyprofessor.get_school_by_name("Drexel University")
    

    def AddProfessor(self, profName):
        professor = ratemyprofessor.get_professor_by_school_and_name(self.school, profName)
        self.professors.append(professor)

    def GetAllProfessors(self):
        list_of_professors = []
        for currentProfessor in self.professors:
            profid = currentProfessor.id
            profName = currentProfessor.name
            overallRating = currentProfessor.rating
            difficulty = currentProfessor.difficulty
            rmp = ratemyprofessor.professor.Professor.get_ratings(currentProfessor)
            ratingMetadata = None
            if (rmp is not None):
                ratingMetadata = json.dumps([rating.__dict__ for rating in rmp], cls=DateTimeEncoder, indent=4)
            
            newProf = Professor.Professor(id=profid, profName=profName, overallRating=overallRating, difficulty=difficulty, metaData=ratingMetadata)
            list_of_professors.append(newProf)
        
        print(len(list_of_professors))
        json_data = json.dumps([eachProfessor.__dict__ for eachProfessor in list_of_professors], indent=4)
        return json_data

    '''professor = ratemyprofessor.get_professor_by_school_and_name(school, "Dimitrios Papadopoulos")

    rmp = ratemyprofessor.professor.Professor.get_ratings(professor)
    
    if professor:
        print(f"Name: {professor.name}")
        print(f"Rating: {professor.rating}")
        print(f"Difficulty: {professor.difficulty}")
        print(f"Number of Ratings: {professor.num_ratings}")
        print(f"Number of Ratings: {professor.id}")
        if professor.would_take_again is not None:
            print(f"Would Take Again: {professor.would_take_again}%")
        else:
            print("Would Take Again: N/A")

    else:
        print("Professor not found.")

    json_data = json.dumps([rating.__dict__ for rating in rmp], cls=DateTimeEncoder, indent=4)
    print(json_data)'''