from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact
from sensor.exception import SensorException
from sensor.logger import logging
import sys, os
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer

class TrainPipeline:

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()


    def start_data_ingestion(self)->DataIngestionArtifact:

        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)

            logging.info("Starting data ingestion")
            
            data_ingestion = DataIngestion(config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            
            return data_ingestion_artifact
        
        except  Exception as e:
            logging.error(f"Error while starting data ingestion: {str(e)}")
            raise  SensorException(f"Error while starting data ingestion: {str(e)}", sys)


    def start_data_validaton(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        
        try:
            logging.info("Starting data validation")
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)

            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config = data_validation_config
            )

            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data validation completed")
            return data_validation_artifact
        
        except  Exception as e:
            logging.error(f"Error while starting data validation: {str(e)}")
            raise SensorException(f"Error while starting data validation: {str(e)}", sys)
        

    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact)-> DataTransformationArtifact:

        try:
            logging.info("Starting Data Transformation")
            data_transformation_config = DataTransformationConfig(training_pipeline_config = self.training_pipeline_config)
            data_transformation = DataTransformation(
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=data_transformation_config
            )

            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation Completed")
            return data_transformation_artifact
        
        except Exception as e:
            SensorException(f"Error while starting data transformation: {str(e)}", sys)


    def start_model_training(self, data_transformation_artifact: DataTransformationArtifact)-> ModelTrainerArtifact:

        try:
            logging.info("Starting Model Training")
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(
                model_trainer_config=model_trainer_config,
                data_transformation_artifact=data_transformation_artifact
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model Training Completed")
            return model_trainer_artifact

        except Exception as e:
            SensorException(f"Error while starting model training: {str(e)}", sys)


    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact=self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact:DataTransformationArtifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact:ModelTrainerArtifact = self.start_model_training(data_transformation_artifact)

        except Exception as e :    
            raise  SensorException(e,sys)

