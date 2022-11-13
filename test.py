# This is script to test some commands and  functions
from dataclasses import dataclass
from gettext import install
from sensor.constants.training_pipeline import SCHEMA_FILE_PATH
from sensor.utils.main_utils import read_yaml_file,write_yaml_file
from sensor.ml.model.estimator import TargetValueMapping
import os
from from_root import from_root
from datetime import datetime
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline
import os
from sensor.constants.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI
from sensor.constants.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File , UploadFile
import pandas as pd
import os
@dataclass
class test_cclass():
    dummy_a:int
    dummy_b:int

object = test_cclass(10,30)

print(object.dummy_a)

"""
Data class the those whicg just the data and dont have any functions , 
please check the above function for more understand
"""


schema_config = read_yaml_file(SCHEMA_FILE_PATH)
print(len(schema_config["columns"]))


print(TargetValueMapping().reverse_mapping())

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_path = os.path.join(from_root() , "logs" , LOG_FILE)
print(logs_path)
print(os.path.join(logs_path, LOG_FILE))


training_pipeline = TrainPipeline()
training_pipeline.run_pipeline()