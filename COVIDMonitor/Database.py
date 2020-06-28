from pymongo import MongoClient


class Database():
    def getDb(self):
        db = MongoClient('localhost', 27017).a2test
        return db
