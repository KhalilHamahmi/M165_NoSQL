from pymongo import MongoClient

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)

""" print(client.server_info()) """



db = client["testdb"]
collection = db["benutzer"]


result = collection.insert_one({"vorname": "Khalil", "nachname": "Hamahmi"})

ausgabe = collection.find_one({"_id": result.inserted_id})
print("Hallo " + ausgabe["vorname"] + " " + ausgabe["nachname"])