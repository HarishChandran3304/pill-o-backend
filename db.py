from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import random
import os
from datetime import datetime, timedelta


load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"), server_api=ServerApi('1'))
db = client["pill-pal"]
prescriptions = db["prescriptions"]
medicines = db["medicines"]
users = db["users"]


def get_prescription(prescription_id: int):
    prescription = prescriptions.find_one({"prescriptionID": prescription_id}, {"_id": 0})
    print(prescription)
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
    prescription = prescriptions.find_one({"prescriptionID": int(prescription_id)}, {"_id": 0})
    verified = prescription["encoding"] == encoding and (datetime.now() - prescription["time"]).seconds < 30
    if verified:
        prescriptions.update_one({"prescriptionID": int(prescription_id)}, {"$set": {"fullfilled": True, "encoding": "success"}})
        return {"verified": True, "prescription": get_prescription(int(prescription_id))}
    else:
        prescriptions.update_one({"prescriptionID": int(prescription_id)}, {"$set": {"encoding": "failure"}})
        return {"verified": False}
    # return {"verified": True, "prescription": prescription}

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

def get_users():
    u = [user for user in users.find({}, {"_id": 0})]
    return {"users": [{"userID": user["userID"], "name": user["userName"]} for user in u]}

def create(prescription):
    prescriptionID = random.randint(1000, 9999)
    prescription["prescriptionID"] = prescriptionID

    doctorID = random.randint(1000, 9999)
    prescription["doctorID"] = doctorID

    for medicine in prescription["medicines"]:
        medicine["medID"] = int(medicine["medID"])
        # medicine["Morning"] = int(medicine["Morning"])
        # medicine["Afternoon"] = int(medicine["Afternoon"])
        # medicine["Night"] = int(medicine["Night"])

    issueDate = datetime.now()
    prescription["issueDate"] = issueDate

    expiryDate = issueDate + timedelta(days=7)
    prescription["expiryDate"] = expiryDate

    prescription["duration"] = 1
    prescription["fullfilled"] = False
    prescription["time"] = None
    prescription["encoding"] = ""

    print(prescription)
    prescriptions.insert_one(prescription)
    user = users.find_one({"userID": prescription["userID"]})
    user["prescriptions"].append(prescriptionID)
    users.update_one({"userID": prescription["userID"]}, {"$set": {"prescriptions": user["prescriptions"]}})