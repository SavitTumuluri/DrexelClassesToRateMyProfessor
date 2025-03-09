import pymongo
import json
import os

uri = "mongodb+srv://suewulin12:Izlfl0VFsWfPotJQ@ratemyprof.oqxbh.mongodb.net/?retryWrites=true&w=majority&appName=RateMyProf",
dbName = "test"

def get_user_choice(collection_name):
    while True:
        choice = input(f"\nFor collection '{collection_name}':\n"
                       "1 - Update (add new documents, keep existing ones)\n"
                       "2 - Clear collection and add new data\n"
                       "3 - Skip update"
                       "Choose (1/2): ").strip()
        if choice in {"1", "2"}:
            return int(choice)
        print("Invalid input. Please enter 1 or 2.")

#def upload_jsons_to_db():
    #take user input and if 1, add, if 2, clear, and if 3, skip. go through for all jsons class, course, professors, and ratings. do only CS for now
    #class_filename = cs_classes.json
    #class_collection = classes