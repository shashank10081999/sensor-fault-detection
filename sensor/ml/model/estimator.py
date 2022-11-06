from sensor.constants.training_pipeline import SAVED_MODEL_DIR , MODEL_FILE_NAME
import os
class TargetValueMapping():
    def __init__(self):
        self.neg : int = 0
        self.pos : int = 1
    
    def to_dict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        return dict(zip(self.__dict__.values() , self.__dict__.keys()))


class SensorModel():

    def __init__(self , preprocessor_object , model_object):
        try:
            self.preprocessor_object = preprocessor_object
            self.model_object = model_object
        except Exception as e:
            raise e
    
    def predict(self,x):
        try:
            x_transformed = self.preprocessor_object.transform(x)
            y_hat = self.model_object.predict(x_transformed)

            return y_hat
        except Exception as e:
            raise e


class ModelResolver():

    def __init__(self,model_dir = SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise e
    
    def get_best_model_path(self):
            try:
                timestamps = list(map(int,os.listdir(self.model_dir)))
                latest_timestamp = max(timestamps)
                latest_model_path = os.path.join(self.model_dir , f"{latest_timestamp}" , MODEL_FILE_NAME)
                return latest_model_path
            except Exception as e:
                raise e

    def is_model_exists(self):
        try:
            if not os.path.exists(self.model_dir):
                return False
            timestamsp = os.listdir(self.model_dir)
            if len(timestamsp) ==0 :
                return False

            latest_model_path  = self.get_best_model_path()

            if not os.path.exists(latest_model_path):
                return False
            return True

        except Exception as e:
            raise e 

