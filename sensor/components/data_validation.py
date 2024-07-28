from distutils import dir_util
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.entity.artifact_entity import DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.utils.main_utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os, sys


class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact) -> None:
        
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            logging.error(f"Error while initializing DataValidation: {str(e)}")
            raise SensorException(f"Error while initializing DataValidation: {str(e)}", sys)
        

    def drop_zero_variance_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        This method is responsible for dropping columns with zero variance
        """
        try:
            logging.info("Dropping columns with zero variance")
            return df.loc[:, df.apply(pd.Series.nunique) != 1]

        except Exception as e:
            logging.error(f"Error while dropping columns with zero variance: {str(e)}")
            raise SensorException(f"Error while dropping columns with zero variance: {str(e)}", sys)
    

    def validate_number_of_columns(self, df: pd.DataFrame) -> bool:
        """
        This method is responsible for validating number of columns
        """
        try:
            logging.info("Validating number of columns")
            logging.info(f"Number of columns in data: {df.shape[1]}")
            logging.info(f"Number of columns in schema: {len(self._schema_config['columns'])}")
            if df.shape[1] != len(self._schema_config['columns']):
                # raise SensorException(f"Number of columns in data is not matching with schema", sys)
                logging.error(f"Number of columns in data is not matching with schema")
                return False
            else:
                return True

        except Exception as e:
            logging.error(f"Error while validating number of columns: {str(e)}")
            raise SensorException(f"Error while validating number of columns: {str(e)}", sys)


    def validate_numerical_columns(self, df: pd.DataFrame) -> bool:
        """
        This method is responsible for validating numerical columns
        """
        try:
            logging.info("Validating numerical columns")
            numerical_column_missing  = False
            missing_numerical_column = []
            numerical_columns = self._schema_config['numerical_columns']
            for column in numerical_columns:
                if column not in df.columns:
                    missing_numerical_column.append(column)
                    numerical_column_missing = True
        
            logging.info(f"Missing numerical columns: {missing_numerical_column}")
            return numerical_column_missing
        
        except Exception as e:
            logging.error(f"Error while validating numerical columns: {str(e)}")
            raise SensorException(f"Error while validating numerical columns: {str(e)}", sys)
        

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        This method is responsible for reading data
        """
        try:
            logging.info("Reading data")
            return pd.read_csv(file_path)
        
        except Exception as e:
            logging.error(f"Error while reading data: {str(e)}")
            raise SensorException(f"Error while reading data: {str(e)}", sys)
        
    
    def validate_dataset_drift(self, df1: pd.DataFrame, df2: pd.DataFrame, threshold=0.05) -> bool:
        """
        This method is responsible for validating dataset drift
        """
        try:
            logging.info("Validating dataset drift")
            drift = False
            report = {}
            for column in df1.columns:
                is_drift = False
                statistic, p_value = ks_2samp(df1[column], df2[column])
                if p_value < threshold:
                    logging.error(f"Drift detected for column: {column}")
                    drift = True
                    is_drift = True
                report.update({column: {"statistic": statistic, "p_value": p_value, "drift": is_drift}})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            drift_report_dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(drift_report_dir_path, exist_ok=True)
            write_yaml_file(drift_report_file_path, report, replace=True)
            
            return drift

        except Exception as e:
            logging.error(f"Error while validating dataset drift: {str(e)}")
            raise SensorException(f"Error while validating dataset drift: {str(e)}", sys) 
    

    def validate_target_column(self, df: pd.DataFrame) -> bool:
        """
        This method is responsible for validating target column
        """
        try:
            logging.info("Validating target column")
            if TARGET_COLUMN not in df.columns:
                logging.error(f"Target column is missing")
                return False
            else:
                return True

        except Exception as e:
            logging.error(f"Error while validating target column: {str(e)}")
            raise SensorException(f"Error while validating target column: {str(e)}", sys)
    
    
    def initiate_data_validation(self) -> DataValidationArtifact:

        """
        This method is responsible for initiating data validation process
        """
        try:
            error_message = ""
    
            logging.info("Initiating data validation process")

            train_df = self.read_data(self.data_ingestion_artifact.train_data_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_data_file_path)

            if not self.validate_number_of_columns(train_df):
                error_message += "Number of columns in training data is not matching with schema\n"
        
            if self.validate_numerical_columns(train_df):
                error_message += "Missing numerical columns in training data\n"

            if not self.validate_target_column(train_df):
                error_message += "Target column is missing in training data\n"
            

            if not self.validate_number_of_columns(test_df):
                error_message += "Number of columns in testing data is not matching with schema\n"
            
            if self.validate_numerical_columns(test_df):
                error_message += "Missing numerical columns in testing data\n"

            if not self.validate_target_column(test_df):
                error_message += "Target column is missing in testing data\n"
            print(error_message)
            if len(error_message) > 0:
                logging.error(f"Error while validating data: {error_message}")
                raise SensorException(error_message, sys)
            
            status = self.validate_dataset_drift(train_df, test_df)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_data_file_path, 
                valid_test_file_path=self.data_ingestion_artifact.test_data_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            ) 

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact

        except SensorException as e:
            logging.error(f"Error while initiating data validation: {str(e)}")
            raise SensorException(f"Error while initiating data validation: {str(e)}", sys)