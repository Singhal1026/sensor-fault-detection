import os

TARGET_COLUMN = 'class'
PIPELINE_NAME = 'sensor'
ARTIFACT_DIR = 'artifact'
FILE_NAME = 'sensor.csv'

TRAINING_DATA_FILE:str = 'train.csv'
TESTING_DATA_FILE: str = 'test.csv'

PREPROCESSING_OBJECT_FILE_NAME = 'preprocessing.pkl'
MODEL_FILE_NAME = 'model.pkl'
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
SCHEMA_DROP_COLS = "drop_columns"


# data ingestion related constant values starts eith DATA_INGESTION

DATA_INGESTION_COLLECTION_NAME: str = 'sensor'
DATA_INGESTION_DATABASE_NAME: str = 'APS'
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store'
DATA_INGESTION_INGESTED_DIR: str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2


# Data Validation related constant values starts with DATA_VALIDATION

DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_VALID_DIR: str = 'valid'
DATA_VALIDATION_INVALID_DIR: str = 'invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE: str = 'report.yaml'


# Data Transformation related constant values starts with DATA_TRANSFORMATION

DATA_TRANSFORMATION_DIR_NAME: str = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = 'transformed_data'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = 'transformed_object'


# Model Trainer related constant values starts with MODEL_TRAINER

MODEL_TRAINER_DIR_NAME: str = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR: str = 'trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME: str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODER_TRAINER_UNDER_FITTING_OVER_FITTING_THRESHOLD: float = 0.05