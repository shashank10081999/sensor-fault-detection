import sys
from typing import Optional
import pandas as pd
import numpy as np
import pandas as pd

from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constants.database import DATABASE_NAME

class SensorData():
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(DATABASE_NAME)
        except Exception as e:
            raise e 
    
    def export_collection_as_dataframe(self,collection_name :  str , database_name : str = None) -> pd.DataFrame:

        try:

            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))

            if "_id" in  df.columns.to_list():
                df = df.drop(["_id"] , axis=1)
            
            df.replace({"na":np.nan} , inplace=True)

            return df

        except Exception as e:
            raise e 



