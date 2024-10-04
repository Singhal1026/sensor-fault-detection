from datetime import datetime
import os
from sensor.constant import training_pipeline

class TrainingPipelineConfig:

    def __init__(self, timestamp:datetime=datetime.now()) -> None:
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_dir = os.path.join(training_pipeline.ARTIFACT_DIR, timestamp)
        self.timestamp = timestamp


class DataIngestionConfig:

    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:
        
        # data ingestion dir path
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME
        )

        # data file path (feature store -> sensor.csv)
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME
        )

        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAINING_DATA_FILE
        )

        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TESTING_DATA_FILE
        )
        
        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME


class DataValidationConfig:

    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:
        
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME
        )

        self.valid_data_dir: str = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR
        )

        self.invalid_data_dir: str = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR
        )

        self.valid_train_file_path : str = os.path.join(
            self.valid_data_dir, training_pipeline.TRAINING_DATA_FILE
        )

        self.valid_test_file_path: str = os.path.join(
            self.valid_data_dir, training_pipeline.TESTING_DATA_FILE
        )

        self.invalid_train_file_path: str = os.path.join(
            self.invalid_data_dir, training_pipeline.TRAINING_DATA_FILE
        )

        self.invalid_test_file_path: str = os.path.join(
            self.invalid_data_dir, training_pipeline.TESTING_DATA_FILE
        ) 

        self.drift_report_dir: str = os.path.join(
            self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR
        )

        self.drift_report_file_path: str = os.path.join(
            self.drift_report_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE
        )

        self.schema_file_path: str = training_pipeline.SCHEMA_FILE_PATH
        self.drop_columns: list = training_pipeline.SCHEMA_DROP_COLS

        
class DataTransformationConfig:

    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:
        
        self.data_transformation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME
        )

        self.transformed_data_dir: str = os.path.join(
            self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR 
        )

        self.transformed_object_dir: str = os.path.join(
            self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR
        )

        self.transformed_train_file_path: str = os.path.join(
            self.transformed_data_dir, training_pipeline.TRAINING_DATA_FILE.replace("csv", "npy")
        )

        self.transformed_test_file_path: str = os.path.join(
            self.transformed_data_dir, training_pipeline.TESTING_DATA_FILE.replace("csv", "npy")
        )

        self.transformed_object_file_path: str = os.path.join(
            self.transformed_object_dir, training_pipeline.PREPROCESSING_OBJECT_FILE_NAME
        )


class ModelTrainerConfig:

    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:
        
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME
        )

        self.trained_model_dir: str = os.path.join(
            self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR
        )

        self.trained_model_file_path: str = os.path.join(
            self.trained_model_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME
        )

        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold: float = training_pipeline.MODER_TRAINER_UNDER_FITTING_OVER_FITTING_THRESHOLD


class ModelEvaluationConfig:

    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:
        
        self.model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.MODEL_EVALUATION_DIR_NAME
        )

        self.report_file_path: str = os.path.join(
            self.model_evaluation_dir, training_pipeline.MODEL_EVALUATION_REPORT_NAME
        )

        self.changed_threshold: float = training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE
    

class ModelPusherConfig:

    def __init__(self, training_pipeline_config:TrainingPipelineConfig) -> None:
        
        self.model_pusher_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.MODEL_PUSHER_DIR_NAME
        )

        self.model_file_path: str = os.path.join(
            self.model_pusher_dir, training_pipeline.MODEL_FILE_NAME
        ) 

        timestamp = round(datetime.now().timestamp())
        
        self.saved_model_path: str = os.path.join(
            training_pipeline.SAVED_MODEL_DIR,
            f"{timestamp}",
            training_pipeline.MODEL_FILE_NAME
        )



  