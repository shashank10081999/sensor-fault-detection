import yaml
import os,sys
import numpy as np
import dill

def read_yaml_file(filepath : str):
    try:
        with open(filepath, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise e 

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path) , exist_ok=True)
        with open(file_path,"w") as f:
            yaml.dump(content , f)
    except Exception as e:
        raise e