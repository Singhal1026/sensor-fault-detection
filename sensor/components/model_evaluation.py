from sensor.exception import SensorException
from sensor.logger import logging

from sensor.entity.artifact_entity import DataValidationArtifact, ModelEvaluationArtifact, ModelTrainerArtifact
from sensor.entity.config_entity import ModelEvaluationConfig, ModelTrainerConfig

from sensor.ml.metric.classification_metric import get_classification_score
from sensor.ml.model.estimater import SensorModel, ModelResolver, TargetValueMapping
from sensor.utils.main_utils import save_object, load_object, write_yaml_file
from sensor.constant.training_pipeline import TARGET_COLUMN

import os, sys
import pandas as pd


class ModelEvaluation:

    def __init__(self, model_trainer_artifact: ModelTrainerArtifact, model_evaluation_config: ModelEvaluationConfig, data_validation_artifact: DataValidationArtifact) -> None:
        self.model_trainer_artifact = model_trainer_artifact
        self.model_evaluation_config = model_evaluation_config
        self.data_validation_artifact = data_validation_artifact
        
    def initiate_model_evaluation(self)-> ModelEvaluationArtifact:
        
        try:
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path
            valid_test_file_path = self.data_validation_artifact.valid_test_file_path

            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)

            df = pd.concat([train_df, test_df])
            y_true = df[TARGET_COLUMN]
            y_true.replace(TargetValueMapping().to_dict(), inplace=True)
            
            df.drop(columns=[TARGET_COLUMN], inplace=True, axis=1)

            train_model_file_path = self.model_trainer_artifact.trained_model_file_path
            model_resolver = ModelResolver()
            is_model_accepted = True

            if not model_resolver.is_model_exists():

                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted,
                    improved_accuracy=None,
                    best_model_path=None,
                    trained_model_path=train_model_file_path,
                    train_model_metric_artifact=self.model_trainer_artifact.train_metric_artifact,
                    best_model_metric_artifact=None
                )

                logging.info(f"Model evaluation completed and artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact
            
            latest_model_path = model_resolver.get_best_model_path()
            latest_model = load_object(latest_model_path)
            train_model = load_object(train_model_file_path)

            y_trained_pred = train_model.predict(df)
            y_latest_pred = latest_model.predict(df)

            trained_metric = get_classification_score(y_true, y_trained_pred)
            latest_metric = get_classification_score(y_true, y_latest_pred)

            improved_accuracy = trained_metric.f1_score - latest_metric.f1_score

            if self.model_evaluation_config.changed_threshold < improved_accuracy:
                is_model_accepeted = True

            else:
                is_model_accepeted = False
            
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                improved_accuracy=improved_accuracy,
                best_model_path=latest_model_path,
                trained_model_path=train_model_file_path,
                train_model_metric_artifact=trained_metric,
                best_model_metric_artifact=latest_metric
            )

            model_eval_report = model_evaluation_artifact.__dict__

            write_yaml_file(self.model_evaluation_config.report_file_path, model_eval_report)
            
            logging.info(f"Model evaluation completed and artifact: {model_evaluation_artifact}")

            return model_evaluation_artifact
        
        except Exception as e:
            logging.error(f"Error while starting model evaluation: {str(e)}")
            raise SensorException(f"Error while starting model evaluation: {str(e)}", sys)
