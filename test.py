# This is script to test some commands and  functions
from dataclasses import dataclass
from gettext import install
from sensor.constants.training_pipeline import SCHEMA_FILE_PATH
from sensor.utils.main_utils import read_yaml_file,write_yaml_file


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
print(schema_config["columns"])