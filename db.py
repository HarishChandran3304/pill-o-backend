from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import random
import os
from datetime import datetime


load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))
db = client["pill-pal"]
prescriptions = db["prescriptions"]
medicines = db["medicines"]
users = db["users"]


def get_prescription(id: int):
    prescription = prescriptions.find_one({"prescriptionID": id}, {"_id": 0})
    for medicine in prescription["medicines"]:
        medID = medicine["medID"]
        medicine.update(get_medicine(medID))
    return prescription

def get_medicine(id: int):
    return medicines.find_one({"medID": id}, {"_id": 0})

def update_encoding(prescription_id: int):
    encoding = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=25))
    prescriptions.update_one({"prescriptionID": prescription_id}, {"$set": {"encoding": encoding, "time": datetime.now()}})
    return {"encoding": encoding}

def verify_encoding(prescription_id: int, encoding: str):
    '''
    Compares the encoding with the one in the database and checks for a 30s time difference
    '''
    prescriptions.update_one({"prescriptionID": prescription_id}, {"$set": {"fullfilled": True, "encoding": "success"}})
    return {"verified": prescriptions.find_one({"prescriptionID": int(prescription_id)}, {"_id": 0})["encoding"] == encoding and (datetime.now() - prescriptions.find_one({"prescriptionID": int(prescription_id)}, {"_id": 0})["time"]).seconds < 30}

def get_user_prescriptions(id: int):
    return {"prescriptions": [get_prescription(prescription_id) for prescription_id in users.find_one({"userID": id}, {"_id": 0})["prescriptions"]]}

def get_medicines():
    return {"medicines": [medicine for medicine in medicines.find({}, {"_id": 0})]}