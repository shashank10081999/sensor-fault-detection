import os,sys
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline
import os
from sensor.constants.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI
from sensor.constants.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File , UploadFile
import pandas as pd
import os


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainPipeline()
        if training_pipeline.is_pipeline_running:
            Response("The training pipeline is already running")
        training_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.get("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(contents)
        model_reslover = ModelResolver()
        if not model_reslover.is_model_exists():
            Response("Model does not exist , Please check the code again")
        best_model_path = model_reslover.get_best_model_path()
        model = load_object(best_model_path)

        y_predicted = model.predict(df)

        df["predicted_column"] = y_predicted

        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)

    except Exception as e:
        raise Response(f"Error Occured! {e}")





if __name__=="__main__":
    #main()
    # set_env_variable(env_file_path)
    app_run(app, host=APP_HOST, port=APP_PORT)
