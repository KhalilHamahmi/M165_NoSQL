from pymongo import MongoClient

class Joke:
    def __init__(self, text, category, author):
        self.text = text
        self.category = category if isinstance(category, list) else [category]
        self.author = author

class Dao_joke:
    def __init__(self):
        self.col = MongoClient("mongodb://localhost:27017/")["jokes_db"]["jokes"]

    def insert(self, joke):
        self.col.insert_one(joke.__dict__)

    def get_category(self, category_name):
        return list(self.col.find({"category": category_name}))

    def delete(self, joke_id):
        self.col.delete_one({"_id": joke_id})