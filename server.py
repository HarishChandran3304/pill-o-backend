from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import get_prescription, get_medicine, update_encoding, verify_encoding, get_user_prescriptions, get_medicines, polling, get_users, create
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:4040",
    "https://positive-clearly-tiger.ngrok-free.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/prescription/{id}")
def prescription(id: int):
    return get_prescription(id)

@app.get("/medicine/{id}")
def medicine(id: int):
    return get_medicine(id)

@app.get("/encoding")
def generate_random_encoding(prescription_id: int):
    if get_prescription(prescription_id)["fullfilled"]:
       return HTTPException(status_code=404, detail="Prescription already fullfilled")
    return update_encoding(prescription_id)

@app.get("/verify")
def verify(encoding_string: str):
    prescription_id, encoding = encoding_string.split("|")
    return verify_encoding(prescription_id, encoding)

@app.get("/users/{id}/prescriptions")
def user_prescriptions(id: int):
    return get_user_prescriptions(id)

@app.get("/medicines")
def medicines():
    return get_medicines()

@app.get("/prescription/{id}/poll")
def poll(id: int):
    return polling(id)

@app.get("/users")
def users():
    return get_users()

class Prescription(BaseModel):
    userID: int
    title: str
    desc: str
    medicines: list

@app.post("/prescriptions")
def create_prescription(prescription: Prescription):
    print(prescription)
    print(dict(prescription))
    create(dict(prescription))
    return {"message": "success"}