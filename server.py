from fastapi import FastAPI
from db import get_prescription, get_medicine, update_encoding, verify_encoding

app = FastAPI()


@app.get("/prescription/{id}")
def prescription(id: int):
    return get_prescription(id)

@app.get("/medicine/{id}")
def medicine(id: int):
    return get_medicine(id)

@app.get("/encoding")
def generate_random_encoding(prescription_id: int):
    return update_encoding(prescription_id)

@app.get("/verify")
def verify(prescription_id: int, encoding: str):
    return verify_encoding(prescription_id, encoding)