from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from sensor.exception import SensorException
from sensor.logger import logging
import sys, os
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation  
from sensor.components.model_pusher import ModelPusher


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


    def start_model_evaluation(self, model_trainer_artifact: ModelTrainerArtifact,  data_validation_artifact: DataValidationArtifact)-> ModelEvaluationArtifact:

        try:
            logging.info("Starting Model Evaluation")

            model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
            
            model_evaluation = ModelEvaluation(
                model_evaluation_config = model_evaluation_config,  
                model_trainer_artifact = model_trainer_artifact,
                data_validation_artifact= data_validation_artifact
            )

            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            logging.info(f"Model Evaluation Completed")
            return model_evaluation_artifact

        except Exception as e:
            SensorException(f"Error while starting model evaluation: {str(e)}", sys)


    def start_model_pusher(self,model_eval_artifact:ModelEvaluationArtifact):
        try:
            logging.info("Starting Model Pusher")

            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config = model_pusher_config, model_evaluation_artifact = model_eval_artifact)
            model_pusher_artifact = model_pusher.initiate_model_pusher()

            logging.info(f"Model Pusher Completed")

            return model_pusher_artifact
        
        except  Exception as e:
            logging.error(f"Error while starting model pusher: {str(e)}")
            raise  SensorException(e,sys)


    def run_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact=self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact:DataTransformationArtifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact:ModelTrainerArtifact = self.start_model_training(data_transformation_artifact)
            model_evaluation_artifact:ModelEvaluationArtifact = self.start_model_evaluation(model_trainer_artifact, data_validation_artifact)

            if not model_evaluation_artifact.is_model_accepted:
                logging.info("Model is not accepted")
                raise Exception("Trained model is not better then best model")
            else:
                logging.info("Model is accepted")

            model_pusher_artifact:ModelPusherArtifact = self.start_model_pusher(model_evaluation_artifact)
                
        except Exception as e :    
            logging.error(f"Error while running pipeline: {str(e)}")
            raise  SensorException(e,sys)

