from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig , DataValidationConfig , DataTransformationConfig , ModelTrainerConfig ,ModelEvaluationConfig,ModelPusherConfig
from sensor.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact , DataTransformationArtifact , ModelTrainerArtficat , ModelEvaluationArtifact,ModelPusherArtifact
import sys,os
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher
from sensor.logger import logging

class TrainPipeline():

    is_pipeline_running = False

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
    
    def start_model_trainer(self , data_transformation_artifact):
        try:
            logging.info("Model training has been started...........................")
            model_trainer_config = ModelTrainerConfig(training_pipeline_config = self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config = model_trainer_config ,data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model Training is completed and the model trainer artifatct : {model_trainer_artifact.__dict__}")
            return model_trainer_artifact
        except  Exception as e:
            raise  e

    def start_model_evaluation(self , model_trainer_artifact , data_validation_artifact):
        try:
            logging.info("Model Evaluation has been started...........................")
            model_evaluation_config = ModelEvaluationConfig(training_pipeline_config = self.training_pipeline_config)
            model_evaluation = ModelEvaluation(model_evaluation_config=model_evaluation_config , model_trainer_artifact=model_trainer_artifact , data_validation_artifact = data_validation_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            logging.info(f"Model Evaluation is completed and the model evaluation artifact : {model_evaluation_artifact.__dict__}")
            return model_evaluation_artifact
        except  Exception as e:
            raise  e

    def start_model_pusher(self,model_evaluation_artifact):
        try:
            logging.info("Model Pusher has been started...........................")
            model_pusher_config = ModelPusherConfig(training_pipeline_config = self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config=model_pusher_config, model_evaluation_artifact=model_evaluation_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info(f"Model Pushing is completed and the model pusher artifact : {model_pusher_artifact.__dict__}")
            return model_pusher_artifact
        except  Exception as e:
            raise  e

    def run_pipeline(self):
        try:
            TrainPipeline.is_pipeline_running = True
            data_ingestion_artifact : DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact : DataValidationArtifact = self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact :  DataTransformationArtifact = self.start_data_transformation(data_validation_artifact = data_validation_artifact)
            model_trainer_artifact : ModelTrainerArtficat = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact : ModelEvaluationArtifact = self.start_model_evaluation(model_trainer_artifact=model_trainer_artifact , data_validation_artifact = data_validation_artifact)
            if not model_evaluation_artifact.is_model_accepted:
                raise Exception("The newly trained model is not better than the model present in the saved model path based the F1 scores of both the models")
            model_pusher_artifact : ModelPusherArtifact = self.start_model_pusher(model_evaluation_artifact = model_evaluation_artifact)
            TrainPipeline.is_pipeline_running = False
        except  Exception as e:
            raise  e
