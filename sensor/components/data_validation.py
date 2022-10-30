from distutils import dir_util
from sensor.constants.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.utils.main_utils import read_yaml_file,write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os,sys

class DataValidation():

    def __init__(self , data_ingestion_artifact: DataIngestionArtifact , data_validation_config : DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise e
    
    def drop_zero_std_columns(self,dataframe)->pd.DataFrame:
        try:
            std_zero_columns = []
            for column in dataframe.columns:
                if np.std(dataframe[column]) == 0:
                    std_zero_columns.append(column)
            
            return dataframe.drop(std_zero_columns , axis=1 , inplace = True)
        except Exception as e:
            raise e
        

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self.schema_config["columns"])

            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise e
    
    def is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self.schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns

            numerical_column_present = True
            missing_numercial_columns = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_column_present = False
                    missing_numercial_columns.append(num_column)
            return numerical_column_present
        except Exception as e:
            raise e
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise e

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                is_same_dist = ks_2samp(d1,d2)

                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            return status
        except Exception as e:
            raise e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:

            error_message = ""

            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            status = self.validate_number_of_columns(dataframe = train_dataframe)

            if not status:
                error_message=f"{error_message}Train dataframe does not contain all columns.\n"

            status = self.validate_number_of_columns(dataframe = test_dataframe)

            if not status:
                error_message=f"{error_message}Test dataframe does not contain all columns.\n"
            
            status = self.is_numerical_column_exist(dataframe= train_dataframe)

            if not status:
                error_message=f"{error_message}Train dataframe does not contain all numerical columns.\n"

            status = self.is_numerical_column_exist(dataframe= test_dataframe)

            if not status:
                error_message=f"{error_message}Test dataframe does not contain all numerical columns.\n"

            if len(error_message) > 0:
                raise Exception(error_message)

            status = self.detect_dataset_drift(train_dataframe, test_dataframe)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            return data_validation_artifact

        except Exception as e:
            raise e


    


