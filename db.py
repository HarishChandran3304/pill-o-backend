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
alerts = db["alerts"]
vaccines = db["vaccines"]


def get_prescription(prescription_id: int) -> dict:
    '''
    DB helper function to fetch prescription details from given prescription ID.
    '''
    prescription = prescriptions.find_one({"prescriptionID": prescription_id}, {"_id": 0})
    for medicine in prescription["medicines"]:
        medID = medicine["medID"]
        medicine.update(get_medicine(medID))
    return prescription

def get_medicine(medID: int) -> dict:
    '''
    DB helper function to fetch medicine details from given medicine ID.
    '''
    return medicines.find_one({"medID": medID}, {"_id": 0})

def update_encoding(prescription_id: int) -> dict:
    '''
    DB helper function to generate a random encoding and update the prescription with it.
    '''
    encoding = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=25))
    prescriptions.update_one({"prescriptionID": prescription_id}, {"$set": {"encoding": encoding, "time": datetime.now()}})
    return {"encoding": encoding}

def verify_encoding(prescription_id: int, encoding: str) -> dict:
    '''
    DB helper function to verify the encoding and return the prescription details if the encoding is correct.
    '''
    prescription = prescriptions.find_one({"prescriptionID": int(prescription_id)}, {"_id": 0})
    verified = prescription["encoding"] == encoding and (datetime.now() - prescription["time"]).seconds < 30
    if verified:
        prescriptions.update_one({"prescriptionID": int(prescription_id)}, {"$set": {"fullfilled": True, "encoding": "success"}})
        return {"verified": True, "prescription": get_prescription(int(prescription_id))}
    else:
        prescriptions.update_one({"prescriptionID": int(prescription_id)}, {"$set": {"encoding": "failure"}})
        return {"verified": False}
    # return {"verified": True, "prescription": prescription}

def get_user_prescriptions(user_id: int) -> dict:
    '''
    DB helper function to fetch all the prescriptions of a user from the given user ID.
    '''
    return {"prescriptions": [get_prescription(prescription_id) for prescription_id in users.find_one({"userID": user_id}, {"_id": 0})["prescriptions"]]}

def get_medicines() -> dict:
    '''
    DB helper function to fetch all medicines.
    '''
    return {"medicines": [medicine for medicine in medicines.find({}, {"_id": 0})]}

def polling(prescription_id: int) -> dict:
    '''
    DB helper function to return the status of the prescription.
    '''
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

def get_users() -> dict:
    '''
    DB helper function to fetch all the users.
    '''
    u = [user for user in users.find({}, {"_id": 0})]
    return {"users": [{"userID": user["userID"], "name": user["userName"]} for user in u]}

def create_prescription(prescription) -> dict:
    '''
    DB helper function to receive a prescription from a doctor, generate missing fields and populate database.
    '''
    prescriptionID = random.randint(1000, 9999)
    prescription["prescriptionID"] = prescriptionID

    doctorID = random.randint(1000, 9999)
    prescription["doctorID"] = doctorID

    for medicine in prescription["medicines"]:
        medicine["medID"] = int(medicine["medID"])

    issueDate = datetime.now()
    prescription["issueDate"] = issueDate

    expiryDate = issueDate + timedelta(days=7)
    prescription["expiryDate"] = expiryDate

    prescription["medNo"] = len(prescription["medicines"])
    prescription["duration"] = 1
    prescription["fullfilled"] = False
    prescription["time"] = None
    prescription["encoding"] = ""
    
    prescriptions.insert_one(prescription)
    user = users.find_one({"userID": prescription["userID"]})
    user["prescriptions"].append(prescriptionID)
    users.update_one({"userID": prescription["userID"]}, {"$set": {"prescriptions": user["prescriptions"]}})

def get_alerts() -> dict:
    '''
    DB helper function to fetch all the alerts.
    '''
    return {"alerts": [alert for alert in alerts.find({}, {"_id": 0})]}

def parse_and_compare_vaccine(time_str, age) -> bool:
    '''
    Given the time of a vaccine and age of the user, returns whether the vaccine is due or not.
    '''
    map = {
        "Birth": 0,
        "6 Weeks": 0.09,
        "10 Weeks": 0.17,
        "14 Weeks": 0.24,
        "9 Months": 0.75,
        "16-24 Months": 1.33,
        "5-6 Years": 5,
        "10 Years": 10,
        "16 Years": 16
    }

    return age > map[time_str]

def get_vaccines(user_id) -> dict:
    '''
    DB helper function to fetch all vaccines.
    '''
    user = users.find_one({"userID": user_id})
    age = user["age"]
    vac = [vaccine for vaccine in vaccines.find({}, {"_id": 0})]
    v = []
    for vaccine in vac:
        vaccine["completed"] = parse_and_compare_vaccine(vaccine["age"], age)
        v.append(vaccine)
    
    return {"vaccines": v}