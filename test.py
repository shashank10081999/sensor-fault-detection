import pymongo 
import pandas as pd

import certifi

ca = certifi.where()


class MongodbOperation:

    def __init__(self) -> None:

        MongoDB_url = "mongodb+srv://shashank:shashank@cluster0.l7igtsr.mongodb.net/?retryWrites=true&w=majority"

        self.client = pymongo.MongoClient(MongoDB_url,tlsCAFile=ca)

        self.db_name="ineuron"

    def select_all(self):
        for i in self.client[self.db_name]["car"].find():
            print(i)


    def pandas_dataframe(self):
        return pd.DataFrame(list(self.client[self.db_name]["car"].find()))


object = MongodbOperation()

df = object.pandas_dataframe()
print(df.describe())

