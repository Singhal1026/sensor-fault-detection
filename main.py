from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os , sys
from sensor.logger import logging

from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.utils.main_utils import load_object, read_yaml_file
from sensor.ml.model.estimater import ModelResolver,TargetValueMapping
from sensor.pipeline import training_pipeline
from sensor.constant.training_pipeline import SAVED_MODEL_DIR

if __name__ == "__main__":

    training_pipeline = TrainPipeline()
    training_pipeline.run_pipeline()
    # app_run(app ,host=APP_HOST,port=APP_PORT)
