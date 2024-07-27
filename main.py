from sensor.exception import SensorException
import sys
import os
from sensor.logger import logging
from sensor.utils2 import dumb_csv_file_to_mongodb_collection
from sensor.pipeline.training_pipeline import TrainPipeline

def test_exception():
    try:
        a = 1/0
    except Exception as e:
        raise SensorException(e, sys)

if __name__ == "__main__":
    # try:
    #     logging.info("Testing exception")
    #     test_exception()
    # except Exception as e:
    #     print(e)
    # file_path = "C:\\Users\\Hello\\PycharmProjects\\ML_project\\sensor-fault-detection\\data\\aps_failure_training_set.csv"
    # database_name = "APS"
    # collection_name = "sensor"
    # dumb_csv_file_to_mongodb_collection(file_path, database_name, collection_name)

    training_pipeline = TrainPipeline()
    training_pipeline.run_pipeline()