from bson import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")


print("Databases")
for name in client.list_database_names():
    print(f" - {name}")

db_name = input("\nSelect Database: ")
db = client[db_name]

print(f"\n{db_name}\n\nCollections")
for col_name in db.list_collection_names():
    print(f" - {col_name}")

collection_name = input("\nSelect Collection: ")
collection = db[collection_name]

print(f"\n{db_name}.{collection_name}\n\nDocuments")
for doc in collection.find():
    print(f" - {doc['_id']}")

id_input = input("\nSelect Document: ")


try:
    target_id = ObjectId(id_input)
except:
    target_id = id_input

selected_doc = collection.find_one({"_id": target_id})

if selected_doc:
    print(f"\n{db_name}.{collection_name}.{selected_doc['_id']}\n")
    for key, value in selected_doc.items():
        if key != "_id":
            print(f"{key}: {value}")
else:
    print("Document not found.")

input("\nPress any button to return")