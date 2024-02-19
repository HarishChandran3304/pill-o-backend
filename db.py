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


def get_prescription(prescription_id: int):
    prescription = prescriptions.find_one({"prescriptionID": prescription_id}, {"_id": 0})
    for medicine in prescription["medicines"]:
        medID = medicine["medID"]
        medicine.update(get_medicine(medID))
    return prescription

def get_medicine(medID: int):
    return medicines.find_one({"medID": medID}, {"_id": 0})

def update_encoding(prescription_id: int):
    encoding = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=25))
    prescriptions.update_one({"prescriptionID": prescription_id}, {"$set": {"encoding": encoding, "time": datetime.now()}})
    return {"encoding": encoding}

def verify_encoding(prescription_id: int, encoding: str):
    verified = {"verified": prescriptions.find_one({"prescriptionID": int(prescription_id)}, {"_id": 0})["encoding"] == encoding and (datetime.now() - prescriptions.find_one({"prescriptionID": int(prescription_id)}, {"_id": 0})["time"]).seconds < 30}
    if verified:
        prescriptions.update_one({"prescriptionID": int(prescription_id)}, {"$set": {"fullfilled": True, "encoding": "success"}})
    else:
        prescriptions.update_one({"prescriptionID": int(prescription_id)}, {"$set": {"encoding": "failure"}})
    return verified

def get_user_prescriptions(user_id: int):
    return {"prescriptions": [get_prescription(prescription_id) for prescription_id in users.find_one({"userID": user_id}, {"_id": 0})["prescriptions"]]}

def get_medicines():
    return {"medicines": [medicine for medicine in medicines.find({}, {"_id": 0})]}

def polling(prescription_id: int):
    prescription = get_prescription(prescription_id)
    fullfilled, encoding = prescription["fullfilled"], prescription["encoding"]
    if encoding == "success" and fullfilled:
        return {"message": "success"}
    elif encoding == "failure":
        return {"message": "failure"}
    elif encoding != "success" and fullfilled:
        return {"message": "fullfilled"}
    else:
        return {"message": "pending"}