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
    classes = "cs_classes.json"
    collection = db["classes"]

    choice = get_user_choice(collection)

    with open(classes, "r", encoding="utf-8") as file:
        data = json.load(file)
        if isinstance(data, dict):  # Ensure data is a list of documents
            data = [data]
    if choice == 2:
        print(f"Clearing collection '{collection}'...")
        collection.delete_many({})

        print(f"Uploading data to '{collection}'...")
        collection.insert_many(data)
        print(f"Successfully updated '{collection}'.")
    
    client.close()
    print("\nAll JSON files have been processed")

upload_class_json_to_db()
