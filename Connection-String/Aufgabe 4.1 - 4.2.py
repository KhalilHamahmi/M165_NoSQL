import os
from pymongo import MongoClient

print(os.environ.get("PATH"))

uri = os.environ.get("MONGODB_URI")
if not uri:
    uri = "mongodb://localhost:27017/"

client = MongoClient(uri)
dbs = client.list_database_names()

for db in dbs:
    print(db)

client.close()