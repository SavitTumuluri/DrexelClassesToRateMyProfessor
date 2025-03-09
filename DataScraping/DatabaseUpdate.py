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

def upload_class_json_to_db():
    client = pymongo.MongoClient(uri)
    db = client[dbName]
    filename = "cs_classes.json"
    collection = db["classes"]

    get_user_choice(collection)