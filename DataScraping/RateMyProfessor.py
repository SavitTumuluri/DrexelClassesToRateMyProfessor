import ratemyprofessor
import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
    
school = ratemyprofessor.get_school_by_name("Drexel University")

def getRatings(name):
    professor = ratemyprofessor.get_professor_by_school_and_name(school, "Dimitrios Papadopoulos")

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
    print(json_data)