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

def save_numpy_array_data(file_path : str , array : np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """

    try:
        dir_path  = os.path.dirname(file_path)
        os.makedirs(dir_path ,exist_ok=True)
        with open(file_path, 'wb') as file_object:
            np.save(file_object, array)
    except Exception as e:
        raise e

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path , "rb") as file_object:
            return np.load(file_object)
    except Exception as e:
        raise e

def save_object(file_path : str, object) -> None:
    try:
        os.makedirs(os.path.dirname(file_path) , exist_ok=True)
        with open(file_path , "wb") as file_object:
            dill.dump(object , file_object)
    except Exception as e:
        raise e

def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The give file path {file_path} does not exist")
        with open(file_path, "rb") as file_object:
            return dill.load(file_object)
    except Exception as e: 
        raise e