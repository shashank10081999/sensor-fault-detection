import os 
import sys
from datetime import datetime 
from sensor.constants import training_pipeline

class TrainingPipelineConfig():

    def __init__(self):
        self.timestamp : str = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.artifact_dir = os.path.join(training_pipeline.ARTIFACT_DIR,self.timestamp)
        self.pipeline_name : str = training_pipeline.PIPELINE_NAME

class DataIngestionConfig():

    def __init__(self , training_pipeline_config : TrainingPipelineConfig):
        self.data_ingestion_dir : str = os.path.join(training_pipeline_config.artifact_dir , training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path : str = os.path.join(self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR , training_pipeline.FILE_NAME)
        self.training_file_path : str = os.path.join(self.data_ingestion_dir , training_pipeline.DATA_INGESTION_DIR_NAME , training_pipeline.TRAIN_FILE_NAME)
        self.testing_file_path : str = os.path.join(self.data_ingestion_dir , training_pipeline.DATA_INGESTION_DIR_NAME , training_pipeline.TEST_FILE_NAME)
        self.train_test_split_ration : float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name : str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
