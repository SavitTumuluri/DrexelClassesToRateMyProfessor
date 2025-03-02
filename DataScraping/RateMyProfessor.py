import ratemyprofessor
import json
import Professor
from pymongo import MongoClient
from bson.objectid import ObjectId
from Encoder import DateTimeEncoder
from datetime import datetime

class RMP:
    def __init__(self):
        self.professors = []
        self.school = ratemyprofessor.get_school_by_name("Drexel University")
        self.client = MongoClient("mongodb+srv://suewulin12:Izlfl0VFsWfPotJQ@ratemyprof.oqxbh.mongodb.net/?retryWrites=true&w=majority&appName=RateMyProf")  # Adjust URI if needed
        self.db = self.client["test"]
        self.professors_collection = self.db["professors"]
        self.ratings_collection = self.db["ratings"]

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

            rating_ids = []
            if (rmp is not None):
                for rating in rmp:
                    rating_dict = rating.__dict__
                    rating_id = self.ratings_collection.insert_one(rating_dict).inserted_id
                    rating_ids.append(rating_id)
                #ratingMetadata = json.dumps([rating.__dict__ for rating in rmp], cls=DateTimeEncoder, indent=4)
            
            professor_doc = {
                "id": profid,
                "name": profName,
                "overallRating": overallRating,
                "difficulty": difficulty,
                "ratingMetadata": rating_ids
            }

            self.professors_collection.insert_one(professor_doc)

            list_of_professors.append(professor_doc)
        
        #print(len(list_of_professors))
        json_data = json.dumps(list_of_professors, default=str, indent=4)
        #self.professors_collection.insert_one(json_data)

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