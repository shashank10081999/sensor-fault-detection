from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
import sys,os
from sensor.components.data_ingestion import DataIngestion

class TrainPipeline():

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except  Exception as e:
            raise e
    
    def start_data_validaton(self):
        try:
            pass
        except  Exception as e:
            raise  e

    def start_data_transformation(self):
        try:
            pass
        except  Exception as e:
            raise  e
    
    def start_model_trainer(self):
        try:
            pass
        except  Exception as e:
            raise  e

    def start_model_evaluation(self):
        try:
            pass
        except  Exception as e:
            raise  e

    def start_model_pusher(self):
        try:
            pass
        except  Exception as e:
            raise  e

    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
        except  Exception as e:
            raise  e