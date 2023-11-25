import io
import pickle
from functools import cache
from typing import List

import numpy as np
import pandas as pd
from fastapi import FastAPI, UploadFile
from fastapi.openapi.models import Response
from pydantic import BaseModel
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import OneHotEncoder, StandardScaler

app = FastAPI()


@cache
def get_model() -> ElasticNet:
    with open('elasticnet.pickle', 'rb') as f:
        return pickle.load(f)


@cache
def get_encoder() -> OneHotEncoder:
    with open('one_hot_encoder.pickle', 'rb') as f:
        return pickle.load(f)


@cache
def get_scaler() -> StandardScaler:
    with open('standard_scaler.pickle', 'rb') as f:
        return pickle.load(f)


class Item(BaseModel):
    name: str
    year: int
    km_driven: int
    fuel: str
    seller_type: str
    transmission: str
    owner: str
    mileage: str
    engine: str
    max_power: str
    torque: str
    seats: float


class Items(BaseModel):
    objects: List[Item]


def predict(df: pd.DataFrame) -> np.array:
    # Normalize
    for column in ('mileage', 'max_power', 'engine'):
        df[column] = pd.to_numeric(df[column].str.partition(' ')[0], errors='coerce',
                                   downcast='float')
    df = df.drop(columns='torque', errors='ignore')

    # One-hot encoding
    categorical_columns = ['fuel', 'seller_type', 'transmission', 'owner', 'seats']
    df_cat = get_encoder().transform(df[categorical_columns])
    df_cat = pd.DataFrame(df_cat, columns=get_encoder().get_feature_names_out())
    df = pd.concat([df.drop(columns=categorical_columns), df_cat], axis=1)

    # scale
    df = pd.DataFrame(get_scaler().fit_transform(df), columns=df.columns.tolist())
    return get_model().predict(df)


@app.post("/predict_item")
def predict_item(item: Item) -> float:
    y_pred = predict(pd.DataFrame([item.model_dump()]))
    return y_pred[0]


@app.post("/predict_items")
def predict_items(file: UploadFile):
    df = pd.read_csv(file.file)
    y_pred = predict(df)
    df = pd.concat([df, y_pred], axis=1)
    buf = io.BytesIO()
    df.to_csv(buf)
    return Response(content=buf.getvalue())
