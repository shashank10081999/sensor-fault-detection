from socket import if_indextoname
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sklearn.model_selection import train_test_split
import os,sys
from pandas import DataFrame
from sensor.data_access.sensor_data import SensorData

class DataIngestion():

    def __init__(self,data_ingestion_config : DataIngestionConfig):

        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise e


    def export_data_into_feature_store(self):

        try:

            sensor_data = SensorData()
            dataframe = sensor_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe

        except  Exception as e:
            raise e

    def split_data_as_train_test(self, dataframe : DataFrame) -> None : 

        try:

            train_data , test_data = train_test_split(dataframe , test_size = self.data_ingestion_config.train_test_split_ration)

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path , exist_ok= True)

            train_data.to_csv(self.data_ingestion_config.training_file_path , index = False , header = True)

            test_data.to_csv(self.data_ingestion_config.testing_file_path , index = False , header = True)

        except Exception as e:
            raise e 

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feature_store()
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise e 


