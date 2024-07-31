import yaml
import pandas as pd
import numpy as np
import os
import sys
import dill
import glob
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


def load_object(file_path: str):
    try:
        logging.info("Entered in load_object method of main_utils.py file")
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
        logging.info("object loaded successfully")
    
    except Exception as e:
        logging.error(f"Error while loading object: {str(e)}")
        raise SensorException(f"Error while loading object: {str(e)}", sys) 
        

def get_latest_preprocessor_path(artifact_dir='artifact', sub_dir='data_transformation/transformed_object', file_name='preprocessing.pkl'):
    try:
        # Get the root directory of the project
        current_dir = os.path.abspath(os.path.dirname(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))

        # Build the full path to the artifact directory
        artifact_path = os.path.join(project_root, artifact_dir)

        logging.info(f"Artifact path: {artifact_path}")

        # Check if artifact directory exists
        if not os.path.exists(artifact_path):
            raise FileNotFoundError(f"Artifact directory not found at path: {artifact_path}")

        logging.info('Artifact directory found')

        # Find all timestamp directories in the artifact directory
        timestamp_dirs = glob.glob(os.path.join(artifact_path, '*'))

        logging.info(f"Found timestamp directories: {timestamp_dirs}")

        # Ensure that there are timestamp directories available
        if not timestamp_dirs:
            raise FileNotFoundError("No timestamp directories found in artifact directory")

        # Get the latest timestamp directory
        latest_timestamp_dir = max(timestamp_dirs, key=os.path.getctime)

        logging.info(f"Latest timestamp directory: {latest_timestamp_dir}")

        # Build the preprocessor path
        preprocessor_path = os.path.join(latest_timestamp_dir, sub_dir, file_name)

        logging.info(f"Preprocessor path: {preprocessor_path}")

        if not os.path.exists(preprocessor_path):
            raise FileNotFoundError(f"Preprocessor file not found at path: {preprocessor_path}")

        return preprocessor_path

    except Exception as e:
        logging.error(f"Error while getting preprocessor path: {str(e)}")
        raise SensorException(e, sys)
