from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import random
import os


load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))
db = client["pill-pal"]
prescriptions = db["prescriptions"]
medicines = db["medicines"]
users = db["users"]


def get_prescription(id: int):
    return prescriptions.find_one({"prescriptionID": id}, {"_id": 0})

def get_medicine(id: int):
    return medicines.find_one({"medID": id}, {"_id": 0})

def update_encoding(prescription_id: int):
    encoding = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=25))
    prescriptions.update_one({"prescriptionID": prescription_id}, {"$set": {"encoding": encoding}})
    return {"encoding": encoding}

def verify_encoding(prescription_id: int, encoding: str):
    return prescriptions.find_one({"prescriptionID": prescription_id}, {"_id": 0})["encoding"] == encoding

def get_user_prescriptions(id: int):
    return [prescriptions.find_one({"prescriptionID": prescription}, {"_id": 0}) for prescription in users.find_one({"userID": id}, {"_id": 0})["prescriptions"]]