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

class user(BaseModel):
    userID: int
    userName: str
    age: int
    prescriptions: list
    bloodGrp: str
    gender: str

class medicine(BaseModel):
    medID: int
    medName: str
    desc: str
    sideEffects: str
    imgNo: int

class alert(BaseModel):
    title: str
    desc: str

