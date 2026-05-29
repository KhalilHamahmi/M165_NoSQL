from pymongo import MongoClient

class Dao_room:
    def __init__(self):
        self.col = MongoClient("mongodb://localhost:27017/")["restaurants"]["rooms"]

    def update(self, room_id, update_data):
        self.col.update_one({"_id": room_id}, {"$set": update_data})

    def delete(self, room_id):
        self.col.delete_one({"_id": room_id})