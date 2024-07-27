import sys
from typing import Optional

import numpy as np
import pandas as pd
import json
from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constant.database import DATABASE_NAME
from sensor.exception import SensorException


class SensorData:

    """ 
    This class is responsible for exporting entire MongoDB data to pandas DataFrame
    """

    def __init__(self):

        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        
        except Exception as e:
            raise SensorException(f"Error while connecting to MongoDB: {str(e)}", sys)
        

    def export_csv_as_collection(self, file_path, collection_name, database_name : Optional [str] = None):
        """
        This method is responsible for export data from CSV file to mongoDB
        """
        try: 
            df = pd.read_csv(file_path)
            df.reset_index(inplace=True, drop=True)
            records = list(json.loads(df.T.to_json()).values())

            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]
            collection.insert_many(records) 
            return len(records)
        except Exception as e:
            raise SensorException(f"Error while exporting data to MongoDB: {str(e)}", sys)
    

    def export_collection_as_dataframe(self, collection_name, database_name : Optional [str] = None)-> pd.DataFrame:
        """
        This method is responsible for exporting entire MongoDB data to pandas DataFrame
        """
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]
            cursor = collection.find()
            df = pd.DataFrame(list(cursor))

            if '_id' in df.columns:
                df.drop(columns=['_id'], inplace=True)

            df.replace({'na': np.nan}, inplace=True)

            return df
        
        except Exception as e:
            raise SensorException(f"Error while exporting data to DataFrame: {str(e)}", sys)