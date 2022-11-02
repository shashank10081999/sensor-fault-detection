from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig , DataValidationConfig , DataTransformationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact , DataTransformationArtifact 
import sys,os
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.logger import logging

class TrainPipeline():

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            logging.info("Starting data ingestion....")
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact.__dict__}")
            return data_ingestion_artifact
        except  Exception as e:
            raise e
    
    def start_data_validaton(self ,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            logging.info("Starting data validation....")
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact = data_ingestion_artifact,data_validation_config = data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation completed and artifact: {data_validation_artifact.__dict__}")
            return data_validation_artifact
        except  Exception as e:
            raise  e

    def start_data_transformation(self , data_validation_artifact : DataValidationArtifact):
        try:

            logging.info("Starting data transformation....")
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)

            data_transformation = DataTransformation(data_validation_artifact , data_transformation_config=data_transformation_config)
            data_transformation_artifact =  data_transformation.initiate_data_transformation()
            logging.info(f"Data Validation completed and artifact: {data_transformation_artifact.__dict__}")
            return data_transformation_artifact
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
            data_ingestion_artifact : DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact : DataValidationArtifact = self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact :  DataTransformationArtifact = self.start_data_transformation(data_validation_artifact = data_validation_artifact)
        except  Exception as e:
            raise  e
