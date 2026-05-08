from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["restaurants"]
col = db["restaurants"]

col.create_index([("address.coord", "2dsphere")])

bezirke = col.distinct("borough")
for b in bezirke:
    print(b)

pipeline = [
    {"$unwind": "$grades"},
    {"$group": {"_id": "$name", "s": {"$avg": "$grades.score"}}},
    {"$sort": {"s": -1}},
    {"$limit": 3}
]
for r in col.aggregate(pipeline):
    print(r["_id"], r["s"])

ref = col.find_one({"name": "Le Perigord"})
if ref:
    pos = ref["address"]["coord"]
    nr = col.find_one({
        "name": {"$ne": "Le Perigord"},
        "address.coord": {"$near": {"$geometry": {"type": "Point", "coordinates": pos}}}
    })
    if nr:
        print(nr["name"])

n = input("Name: ")
k = input("Küche: ")
f = {}
if n:
    f["name"] = {"$regex": n, "$options": "i"}
if k:
    f["cuisine"] = {"$regex": k, "$options": "i"}

for res in col.find(f):
    print(res["name"], "|", res["cuisine"])