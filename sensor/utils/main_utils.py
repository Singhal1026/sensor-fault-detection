import yaml
import pandas as pd
import numpy as np
import os
import sys
import dill
from sensor.exception import SensorException
import logging


def read_yaml_file(file_path:str)->dict:
    """
    This method is responsible for reading YAML file
    """
    try:
        with open(file_path, 'r') as stream:
            return yaml.safe_load(stream)
    except Exception as e:
        logging.error(f"Error while reading YAML file: {str(e)}")
        raise SensorException(f"Error while reading YAML file: {str(e)}", sys)
    

def write_yaml_file(file_path:str, content:object, replace:bool = False)-> None:
    """
    This method is responsible for creating yaml file
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)

    except Exception as e:
        logging.error(f"Error while writing YAML file: {str(e)}")
        raise SensorException(f"Error while writing YAML file: {str(e)}", sys)
    

def save_numpy_array_data(file_path:str, data:np.array)-> None:
    """
    This method is responsible for saving numpy array data
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, data)
    except Exception as e:
        logging.error(f"Error while saving numpy array data: {str(e)}")
        raise SensorException(f"Error while saving numpy array data: {str(e)}", sys)
    
def load_numpy_array_data(file_path:str)-> np.array:
    """
    This method is responsible for loading numpy array data
    """
    try:
        with open(file_path, 'rb') as file:
            return np.load(file)
    except Exception as e:
        logging.error(f"Error while loading numpy array data: {str(e)}")
        raise SensorException(f"Error while loading numpy array data: {str(e)}", sys)
    

def save_object(file_path: str, obj: object):
    try:
        logging.info("Entered in save_object method of main_utils.py file")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
        logging.info("object saved successfully")
    
    except Exception as e:
        logging.error(f"Error while saving object: {str(e)}")
        raise SensorException(f"Error while saving object: {str(e)}", sys)
        