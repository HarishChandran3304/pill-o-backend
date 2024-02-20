from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import get_prescription, get_medicine, update_encoding, verify_encoding, get_user_prescriptions, get_medicines, polling, get_users, create_prescription, get_alerts, get_vaccines, create_doctor
from models import enteredPrescription, generatedPrescription, Doctor

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
def prescription(id: int) -> dict:
    '''
    METHOD: GET
    ENDPOINT: /prescription/{id}
    Path parameter: id (int)
    Given a prescription id, returns the prescription details.
    '''
    return get_prescription(id)

@app.get("/medicine/{id}")
def medicine(id: int) -> dict:
    '''
    METHOD: GET
    ENDPOINT: /medicine/{id}
    Path parameter: id (int)
    Given a medicine id, returns the medicine details.
    '''
    return get_medicine(id)

@app.get("/encoding")
def generate_random_encoding(prescription_id: int) -> dict:
    '''
    METHOD: GET
    ENDPOINT: /encoding
    Query parameter: prescription_id (int)
    Given a prescription id, generates a random encoding and updates the prescription with it.
    '''
    if get_prescription(prescription_id)["fullfilled"]:
       return HTTPException(status_code=404, detail="Prescription already fullfilled")
    return update_encoding(prescription_id)

@app.get("/verify")
def verify(encoding_string: str) -> dict:
    '''
    METHOD: GET
    ENDPOINT: /verify
    Query parameter: encoding_string (str)
    Given a string of the form "prescription_id|encoding", verifies the encoding and returns the prescription details if the encoding is correct.
    '''
    prescription_id, encoding = encoding_string.split("|")
    return verify_encoding(prescription_id, encoding)

@app.get("/users/{id}/prescriptions")
def user_prescriptions(id: int) -> dict:
    '''
    METHOD: GET
    ENDPOINT: /users/{id}/prescriptions
    Path parameter: id (int)
    Given a user id, returns all the prescriptions of the user.
    '''
    return get_user_prescriptions(id)

@app.get("/medicines")
def medicines() -> dict:
    '''
    METHOD: GET
    ENDPOINT: /medicines
    Returns all the medicines in the database.
    '''
    return get_medicines()

@app.get("/prescription/{id}/poll")
def poll(id: int) -> dict:
    '''
    METHOD: GET
    ENDPOINT: /prescription/{id}/poll
    Path parameter: id (int)
    Given a prescription id, returns the status of the prescription.
    '''
    return polling(id)

@app.get("/users")
def users() -> dict:
    '''
    METHOD: GET
    ENDPOINT: /users
    Returns all the users in the database.
    '''
    return get_users()

@app.post("/prescriptions")
def create(prescription: enteredPrescription) -> dict:
    '''
    METHOD: POST
    ENDPOINT: /prescriptions
    Request body:
        userID (int)
        title (str)
        desc (str)
        medicines (list)
    Given a prescription, creates a new prescription and returns a success message.
    '''
    create_prescription(dict(prescription))
    return {"message": "success"}

@app.get("/alerts")
def alerts() -> dict:
    '''
    METHOD: GET
    ENDPOINT: /alerts
    Returns all the alerts in the database.
    '''
    return get_alerts()

@app.get("/users/{id}/vaccines")
def vaccines(id: int) -> dict:
    '''
    METHOD: GET
    ENDPOINT: /vaccines
    Query Parameter: id (int)
    Given a user id, returns all the vaccines for the user.
    '''
    return get_vaccines(id)

@app.post("/doctors")
def doctor(doc: Doctor) -> dict:
    '''
    METHOD: POST
    ENDPOINT: /doctors
    Request body:
        doctorID (int)
        doctorName (str)
        age (int)
    Given a doctor, creates a new doctor and returns a success message.
    '''
    create_doctor(dict(doc))
    return {"message": "success"}