import io
import pickle
from contextlib import asynccontextmanager
from functools import cache, partial
from typing import List

import numpy as np
import pandas as pd
import uvicorn as uvicorn
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from starlette.responses import StreamingResponse


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


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_model()
    get_scaler()
    get_encoder()
    yield


app = FastAPI(lifespan=lifespan)


def predict(df: pd.DataFrame) -> np.array:
    # Normalize
    for column in ('mileage', 'max_power', 'engine'):
        df[column] = pd.to_numeric(df[column].str.partition(' ')[0], errors='coerce',
                                   downcast='float')
    df = df.drop(columns=['torque', 'name'], errors='ignore')

    # One-hot encoding
    categorical_columns = ['fuel', 'seller_type', 'transmission', 'owner', 'seats']
    df_cat = get_encoder().transform(df[categorical_columns])
    df_cat = pd.DataFrame(df_cat, columns=get_encoder().get_feature_names_out())
    df = pd.concat([df.drop(columns=categorical_columns), df_cat], axis=1)

    # scale
    df = pd.DataFrame(get_scaler().transform(df), columns=df.columns.tolist())
    return get_model().predict(df)


@app.post("/predict_item")
def predict_item(item: Item) -> float:
    y_pred = predict(pd.DataFrame([item.model_dump()]))
    return y_pred[0]


@app.post("/predict_items")
def predict_items(file: UploadFile):
    df = pd.read_csv(file.file)
    y_pred = predict(df)
    y_pred = pd.DataFrame(y_pred, columns=['selling_price'])
    df = pd.concat([df, y_pred], axis=1)
    buf = io.BytesIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    headers = {
        'Content-Disposition': 'attachment; filename="result.csv"'
    }
    return StreamingResponse(iter(partial(buf.read, 8 * 2 ** 10), b''), headers=headers)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)
