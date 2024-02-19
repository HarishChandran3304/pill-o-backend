from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os


load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))
db = client["pill-pal"]
prescriptions = db["prescriptions"]
medicines = db["medicines"]


def get_prescription(id: int):
    return prescriptions.find_one({"prescriptionID": id}, {"_id": 0})

def get_medicine(id: int):
    return medicines.find_one({"medID": id}, {"_id": 0})