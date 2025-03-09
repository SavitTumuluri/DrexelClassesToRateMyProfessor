import pymongo
import json
import os

uri = "mongodb+srv://suewulin12:Izlfl0VFsWfPotJQ@ratemyprof.oqxbh.mongodb.net/?retryWrites=true&w=majority&appName=RateMyProf",
dbName = "test"

def upload_class_json_to_db():
    client = pymongo.MongoClient(uri)
    db = client(dbName)
    filename = ""
    