# This is script to test some commands and  functions
from dataclasses import dataclass
from gettext import install
from sensor.constants.training_pipeline import SCHEMA_FILE_PATH
from sensor.utils.main_utils import read_yaml_file,write_yaml_file
from sensor.ml.model.estimator import TargetValueMapping
import os
from from_root import from_root
from datetime import datetime
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