from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os , sys
from sensor.logger import logging

from sensor.entity.artifact_entity import DataTransformationArtifact
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.utils.main_utils import load_object, read_yaml_file, get_latest_preprocessor_path
from sensor.ml.model.estimater import ModelResolver,TargetValueMapping
from sensor.pipeline import training_pipeline
from sensor.constant.training_pipeline import SAVED_MODEL_DIR

from  fastapi import FastAPI
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Response
import pandas as pd
import numpy as np


app = FastAPI()



origins = ["*"]
#Cross-Origin Resource Sharing (CORS) 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/",tags=["authentication"])
async def  index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train():
    try:

        training_pipeline = TrainPipeline()

        if training_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        
        training_pipeline.run_pipeline()
        return Response("Training successfully completed!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")
        

@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> Response:
    try:
        logging.info("reading csv file")
        df = pd.read_csv(file.file)

        if df.empty:
            logging.error("Uploaded file is empty")
            return Response("Uploaded file is empty", status_code=400)\
        
        # replcaing na with np.nan
        df.replace('na', np.nan, inplace=True)

        # get required columns
        logging.info("reading schema file")
        schema_file_path = os.path.join("config", "schema.yaml")
        schema = read_yaml_file(schema_file_path)

        # Extract column names from schema
        logging.info("extracting required columns")
        schema_columns = schema.get('columns', [])
        logging.info(f"Schema columns: {schema_columns}")
        required_columns = [list(data.keys())[0] for data in schema_columns if list(data.values())[0] != 'category']
        logging.info(f"Required columns: {required_columns}")

        logging.info("checking missing columns")
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logging.error(f"Missing columns in input file: {missing_columns}")
            return Response(f"Missing columns in input file: {missing_columns}", status_code=400)

        logging.info("filtering required columns")
        df = df[required_columns]

        # Get the preprocessor path
        preprocessor_path = get_latest_preprocessor_path()
        if not os.path.exists(preprocessor_path):
            logging.error("Preprocessor is not available")
            return Response("Preprocessor is not available", status_code=500)

        # Load the model
        logging.info("loading model")
        Model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not Model_resolver.is_model_exists():
            logging.info("Model is not available")
            return Response("Model is not available")
        
        logging.info("loading preprocessor and transforming data")
        preprocessor = load_object(file_path=preprocessor_path)
        df_transformed = preprocessor.transform(df)

        logging.info("loading model")
        best_model_path = Model_resolver.get_best_model_path()
        model= load_object(file_path=best_model_path)

        logging.info("mapping target values")
        target_mapping = TargetValueMapping().reverse_mapping()

        logging.info("predicting data")
        y_pred=model.predict(df_transformed)
        logging.info(f'Prediction done and y_pred is {y_pred}')
        df['predicted_column'] = y_pred

        logging.info("mapping predicted values")
        df['predicted_column'] = df['predicted_column'].map(target_mapping)

        # Convert DataFrame to CSV and return as response
        logging.info("converting dataframe to csv")
        response_df = df.to_csv(index=False)
        return Response(content=response_df, media_type="text/csv", headers={"Content-Disposition": "attachment;filename=predictions.csv"})

    except  Exception as e:
        return Response(f"Error Occurred: {e}", status_code=500)

def main():
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__ == "__main__":

    app_run(app ,host=APP_HOST,port=APP_PORT)
