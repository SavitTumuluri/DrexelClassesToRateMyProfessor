from pymongo import MongoClient

config = {
    "uri" : "mongodb+srv://suewulin12:Izlfl0VFsWfPotJQ@ratemyprof.oqxbh.mongodb.net/?retryWrites=true&w=majority&appName=RateMyProf",
    "dbName": "test"
}

def connect_to_mongo():
    try:
        client = MongoClient(config["uri"])
        db = client[config["dbName"]]

        collection = db["classes"]
        documents = collection.find()

        for doc in documents:
            print(doc)

        client.close()
        return True

    except:
        print("Fail to connect to database")

if __name__ == "__main__":
    connection_success = connect_to_mongo()
    print(f"Connection Successful: {connection_success}")
