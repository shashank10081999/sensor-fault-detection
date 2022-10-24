from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constants.database import DATABASE_NAME
import pandas as pd

if __name__ == '__main__':
    mongoDB_client = MongoDBClient()
    print("collection names : " , mongoDB_client.database.list_collection_names())

    df = pd.DataFrame(list(mongoDB_client.database["car"].find()))

    df.to_csv("notebooks/aps_failure_training_reduced.csv")