
from bson import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

while True:
    dbs = client.list_database_names()
    if not dbs:
        print("No Database")
        input("\nPress any button to return")
        continue

    print("\nDatabases")
    for name in dbs:
        print(f" - {name}")

    while True:
        db_name = input("\nSelect Database: ")
        if db_name in dbs:
            break
        print("Datenbank nicht gefunden.")

    db = client[db_name]
    cols = db.list_collection_names()
    if not cols:
        print(f"\n{db_name}\n\nNo Collection")
        input("\nPress any button to return")
        continue

    print(f"\n{db_name}\n\nCollections")
    for col_name in cols:
        print(f" - {col_name}")

    while True:
        collection_name = input("\nSelect Collection: ")
        if collection_name in cols:
            break
        print("Collection nicht gefunden.")

    collection = db[collection_name]
    docs = list(collection.find())
    if not docs:
        print(f"\n{db_name}.{collection_name}\n\nNo Document")
        input("\nPress any button to return")
        continue

    print(f"\n{db_name}.{collection_name}\n\nDocuments")
    for doc in docs:
        print(f" - {doc['_id']}")

    while True:
        id_input = input("\nSelect Document: ")
        try:
            target_id = ObjectId(id_input) if ObjectId.is_valid(id_input) else id_input
        except:
            target_id = id_input

        selected_doc = collection.find_one({"_id": target_id})
        if selected_doc:
            print(f"\n{db_name}.{collection_name}.{selected_doc['_id']}\n")
            for key, value in selected_doc.items():
                if key != "_id":
                    print(f"{key}: {value}")
            break
        print("Document ID nicht gefunden.")

    input("\nPress any button to return")