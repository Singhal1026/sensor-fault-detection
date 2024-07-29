import os
import sys
from sensor.exception import SensorException

class TargetValueMapping:

    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1


    def to_dict(self):
        return self.__dict__ 
    

    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))
    

class SensorModel:

    def __init__(self, preprocessor, model) -> None:
        try:
            self.preprocesser = preprocessor
            self.model = model
        except Exception as e:
            raise SensorException(f"Error while initializing SensorModel: {str(e)}", sys)
        
    
    def predict(self, data):
        try:
            x_transform = self.preprocesser.transform(data)
            y_hat = self.model.predict(x_transform)
            return y_hat
        
        except Exception as e:
            raise SensorException(f"Error while predicting data: {str(e)}", sys)