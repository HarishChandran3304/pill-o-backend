from fastapi import FastAPI
from db import get_prescription, get_medicine

app = FastAPI()


@app.get("/prescription/{id}")
def prescription(id: int):
    return get_prescription(id)

@app.get("/medicine/{id}")
def medicine(id: int):
    return get_medicine(id)