from fastapi import FastAPI
from db import get_prescription

app = FastAPI()


@app.get("/prescription/{id}")
def prescription(id: int):
    return get_prescription(id)