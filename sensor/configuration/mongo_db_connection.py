import pymongo
from sensor.constants.database import DATABASE_NAME
import certifi
import os

ca = certifi.where()


class MongoDBClient():
    client = None

    def __init__(self,database_name = DATABASE_NAME):

        try:
            if MongoDBClient.client is None:

                mongoDB_url = os.getenv("MONGODB")

                MongoDBClient.client = pymongo.MongoClient(mongoDB_url,tlsCAFile=ca)

                self.client = MongoDBClient.client

                self.database_name = database_name

                self.database = self.client[database_name]

        except Exception as e:
            raise e


