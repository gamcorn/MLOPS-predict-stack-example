"""This is the prediction server that will prepare the request for the
MlFlow server model prediction scheme.
"""
# pylint: disable=no-name-in-module, too-few-public-methods

import logging
from logging.config import dictConfig
from typing import Union

import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pandas import DataFrame
from pydantic import BaseModel

from app.settings import conf, log_conf

dictConfig(log_conf.dict())
logger = logging.getLogger("ml-app")

app = FastAPI(debug=True)


class FormRequest(BaseModel):
    """Representation of the data sent by the form with some checks
    that are difficult to be performed by streamlit.
    """

    cylinders: Union[float, int]
    displacement: Union[float, int]
    horsepower: Union[float, int]
    weight: Union[float, int]
    acceleration: Union[float, int]
    model_year: Union[float, int]
    origin: Union[float, int]


def predict_risk(data: DataFrame):
    """Calls the mlflow prediction module with the given model."""
    mlflow.set_tracking_uri(conf.MLFLOW_URL)

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(conf.LOGGED_MODEL)

    # Predict on a Pandas DataFrame.
    try:
        return loaded_model.predict(pd.DataFrame(data))
    except Exception as exc:
        raise HTTPException(418, "Data provided is untreatable") from exc


@app.post("/make_prediction")
async def calculate_risk(form_request: FormRequest):
    """Prepares data from user and gets a prediction."""
    logger.info("Entering backend with data: %s", form_request.dict())
    data = pd.DataFrame(form_request.dict(), index=[0])
    return predict_risk(data)[0]
