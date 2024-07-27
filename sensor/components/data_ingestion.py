from sensor.exception import SensorException
from sensor.logger import  logging
import os
import sys
from pandas import DataFrame
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.data_access.sensor_data import SensorData
from sklearn.model_selection import train_test_split
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import SCHEMA_FILE_PATH

class DataIngestion:
    def __init__(self, config: DataIngestionConfig) -> None:
        self.config = config
        self.sensor_data = SensorData()
        self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

    def export_data_into_feature_store(self)->DataFrame:
        """
        Export MongoDB data as DataFrame into feature store
        """

        try:
            logging.info("Exporting data from MongoDB into feature store")

            sensor_data = SensorData()
            df = sensor_data.export_collection_as_dataframe(self.config.collection_name)

            featur_store_file_path = self.config.feature_store_file_path
            dir_path = os.path.dirname(featur_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            df.to_csv(featur_store_file_path, index=False, header=True)
            return df

        except SensorException as e:
            logging.error(f"Error while exporting data into feature store: {str(e)}")
            raise SensorException(f"Error while exporting data into feature store: {str(e)}", sys)

    def split_data_as_train_test(self, dataframe: DataFrame):
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.config.train_test_split_ratio, random_state=42) 
            
            logging.info(f"Splitting data into train and test set with ratio: {self.config.train_test_split_ratio}")

            train_dir_path = os.path.dirname(self.config.training_file_path)
            test_dir_path = os.path.dirname(self.config.testing_file_path)

            os.makedirs(train_dir_path, exist_ok=True)
            os.makedirs(test_dir_path, exist_ok=True)

            logging.info(f"Saving train data at: {self.config.training_file_path}")
            logging.info(f"Saving test data at: {self.config.testing_file_path}")

            train_set.to_csv(self.config.training_file_path, index=False, header=True)
            test_set.to_csv(self.config.testing_file_path, index=False, header=True)

            logging.info("Data split and saved successfully")
        
        except Exception as e:
            logging.error(f"Error while splitting data into train and test set: {str(e)}")
            raise SensorException(f"Error while splitting data into train and test set: {str(e)}", sys)

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        """
        This method is responsible for initiating data ingestion process
        """
        try:
            logging.info("Initiating data ingestion process")
            df = self.export_data_into_feature_store()
            df = self._preprocess_data(df)
            self.split_data_as_train_test(df)
            logging.info("Data ingestion process completed successfully")
            return DataIngestionArtifact(train_data_file_path=self.config.training_file_path, test_data_file_path=self.config.testing_file_path)
        
        except SensorException as e:
            logging.error(f"Error while initiating data ingestion: {str(e)}")
            raise SensorException(f"Error while initiating data ingestion: {str(e)}", sys)


    def _preprocess_data(self, df: DataFrame) -> DataFrame:
        try:
            df = df.dropna()
            df = df.drop_duplicates()
            df = df.sample(frac=1).reset_index(drop=True)
            df = df.drop(columns=self._schema_config['drop_columns'], axis=1)  
            return df
        except Exception as e:
            logging.error(f"Error while preprocessing data: {str(e)}")
            raise SensorException(f"Error while preprocessing data: {str(e)}", sys)
 