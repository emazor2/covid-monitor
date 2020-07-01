from pymongo import MongoClient


class Database():
    def getDb(self):
        """Connects to the MongoDB database."""
        db = MongoClient('localhost', 27017).a2test
        return db
