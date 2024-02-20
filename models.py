from pydantic import BaseModel

class enteredPrescription(BaseModel):
    userID: int
    title: str
    desc: str
    medicines: list

class generatedPrescription(BaseModel):
    prescriptionID: int
    title: str
    desc: str
    medicines: list
    encoding: str
    time: str

class vaccines(BaseModel):
    age: str
    vaccines: list

class User(BaseModel):
    userID: int
    userName: str
    age: int
    prescriptions: list
    bloodGrp: str
    gender: str

class Medicine(BaseModel):
    medID: int
    medName: str
    desc: str
    sideEffects: str
    imgNo: int

class Alert(BaseModel):
    title: str
    desc: str

class Doctor(BaseModel):
    docID: int
    name: str
    age: int
    speciality: str