from pymongo import MongoClient
from typing import List

class Database:
    def __init__(self, db_name: str):
        self.client = MongoClient()
        self.db = self.client[db_name]
    
    def create_collection(self, collection_name: str):
        self.table = self.db[collection_name]
        return self.table

    def get_collection(self, collection_name: str):
        collist = self.db.list_collection_names()
        if collection_name in collist:
            return self.db[collection_name]
        else: 
            return None
    
    def insert(self, collection_name: str, document: List[dict]):
        collection = self.get_collection(collection_name)
        if collection:
            collection.insert_many(document)

