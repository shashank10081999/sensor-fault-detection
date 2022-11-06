from sensor.utils.main_utils import load_numpy_array_data
from sensor.logger import logging
from sensor.entity.artifact_entity import DataTransformationArtifact , ModelTrainerArtficat
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.ml.metrics.classfication_metric import get_classification_metrics
from sensor.utils.main_utils import load_object , save_object
from sensor.ml.model.estimator import SensorModel
from xgboost import XGBClassifier
class ModelTrainer():
    def __init__(self , model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact) -> None:
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise e

    def train_model(self,x_train,y_train):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x_train,y_train)
            return xgb_clf
        except Exception as e:
            raise e


    def initiate_model_trainer(self) -> ModelTrainerArtficat:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # Loading the train and test array 
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train , y_train , x_test , y_test = (train_arr[:,:-1] , train_arr[:,-1] , test_arr[:,:-1] ,test_arr[:,-1])

            model = self.train_model(x_train,y_train)

            y_train_predicted = model.predict(x_train)

            classification_train_metric = get_classification_metrics(y_train , y_train_predicted)

            if classification_train_metric.f1_score <= self.model_trainer_config.expected_accuracy:
                raise Exception("Based on the Train F1 score the model is Under Fitting")

            y_test_predicted = model.predict(x_test)

            classification_test_metric = get_classification_metrics(y_test , y_test_predicted)

            diff = abs(classification_train_metric.f1_score - classification_test_metric.f1_score)

            if diff >= self.model_trainer_config.overfitting_underfitting_threshold:
                raise Exception("Based on the Difference between training f1 score and test f1 score the model is over fitting")

            preprocessor_object_file_path = self.data_transformation_artifact.transformed_object_file_path

            preprocessor_object = load_object(preprocessor_object_file_path)

            sensor_object = SensorModel(preprocessor_object , model)

            save_object(file_path=self.model_trainer_config.trained_model_file_path , object = sensor_object)

            model_trainer_artficat = ModelTrainerArtficat(trained_model_file_path= self.model_trainer_config.trained_model_file_path,train_metric_artifact=classification_train_metric , test_metric_artifact=classification_test_metric)

            logging.info(f"model trainer artifact {model_trainer_artficat.__dict__}")

            return model_trainer_artficat

        except Exception as e:
            raise e