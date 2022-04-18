#from bson.binary import UuidRepresentation
from uuid import uuid4
from pandas import DataFrame

class db_mongo:

    def __init__(self):
        print("Init DB")

        self.db = self.get_database()

        self.db["text_parts_content_resumes"]

        self.db["text_full_resumes"]

    def get_database(self):

        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = "mongodb://dbOwnerRR:123456@localhost:27017/?authSource=dbResumesRecommender"

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        from pymongo import MongoClient
        client = MongoClient(CONNECTION_STRING, uuidRepresentation='standard')

        # Create the database for our example (we will use the same database throughout the tutorial
        return client['dbResumesRecommender']

    def insert_text(self, object):

        collection = self.db["text_parts_content_resumes"]

        uuid_obj = uuid4()

        object["_id"] = uuid_obj

        collection.insert_many([object])

    def get_text(self, top):
        collection = self.db["text_parts_content_resumes"]

        #item_details = collection.find()

        #item_details = collection.aggregate([{"$sort": {"text": 1}},{"$limit": 5}])



        item_details = collection.find({},{ "_id": 1, "text": 2, "class": 3 }).limit(top)

        items_df = DataFrame(list(item_details))

        return items_df

    def insert_text_full_resume(self, object):

        collection = self.db["text_full_resumes"]

        uuid_obj = uuid4()

        object["_id"] = uuid_obj

        collection.insert_many([object])

    def get_text_full_resume(self, top):
        collection = self.db["text_full_resumes"]

        #item_details = collection.find()

        #item_details = collection.aggregate([{"$sort": {"text": 1}},{"$limit": 5}])



        item_details = collection.find({},{ "_id": 1, "text": 2, "class": 2 }).limit(top)

        items_df = DataFrame(list(item_details))

        return items_df

    def clean_text_full_resumes(self):
        collection = self.db["text_full_resumes"]

        collection.delete_many({})
