from sensor.logger import logging
from sensor.entity.artifact_entity import ModelPusherArtifact , ModelEvaluationArtifact
from sensor.entity.config_entity import ModelEvaluationConfig , ModelPusherConfig
import shutil
import os

class ModelPusher():

    def __init__(self,model_pusher_config:ModelPusherConfig,model_evaluation_artifact: ModelEvaluationArtifact):
        try:

            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact
        except Exception as e:
            raise e

    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            train_model_file_path = self.model_evaluation_artifact.trained_model_path

            model_file_path = self.model_pusher_config.model_file_path
            os.makedirs(os.path.dirname(model_file_path) , exist_ok=True)
            shutil.copy(src=train_model_file_path,dst=model_file_path)

            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path))
            shutil.copy(src=train_model_file_path,dst=saved_model_path)

            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path,model_file_path=model_file_path)

            return model_pusher_artifact

        except Exception as e:
            raise e 
            