from fastapi import FastAPI, Response, Request, Query, Cookie, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import HTMLResponse
from fastapi_mako import FastAPIMako
from fastapi.templating import Jinja2Templates
import hashlib
from datetime import date, timedelta

app = FastAPI()
app.counter = 0


class HelloResp(BaseModel):
    msg: str


# example

@app.get('/counter')
def counter():
    app.counter += 1
    return app.counter


@app.get("/hello/{name}", response_model=HelloResp)
async def read_item(name: str):
    return HelloResp(msg=f"Hello {name}")


# task 1.1

@app.get("/")
def root():
    return {"message": "Hello world!"}


# task 1.2
@app.get("/method", status_code=200)
@app.post("/method", status_code=201)
@app.delete("/method", status_code=200)
@app.put("/method", status_code=200)
@app.options("/method", status_code=200)
def read_request(request: Request):
    return {"method": request.method}


# task 1.3
@app.get("/auth", status_code=401)
def get_auth(password: Optional[str] = None, password_hash: Optional[str] = None):
    if not password or not password_hash or hashlib.sha512(str(password).encode("utf-8")).hexdigest() != str(
            password_hash):
        return Response(status_code=401)
    else:
        return Response(status_code=204)


# task 1.4
app.patient_id = 1
app.patients = {}


class PatientIn(BaseModel):
    name: str
    surname: str


class PatientOut(BaseModel):
    id: int
    name: str
    surname: str
    register_date: date
    vaccination_date: date


@app.post("/register", status_code=201)
def post_register(patient: PatientIn):
    patient_id = app.patient_id
    app.patient_id += 1
    tmpDate = date.today()
    register_date = tmpDate.strftime("%Y-%m-%d")
    length_name_plus_surname = len([letter for letter in patient.name + patient.surname if letter.isalpha()])
    vaccination_date = (tmpDate + timedelta(days=length_name_plus_surname)).strftime("%Y-%m-%d")

    patient_out = PatientOut(
        id=patient_id,
        name=patient.name,
        surname=patient.surname,
        register_date=register_date,
        vaccination_date=vaccination_date
    )
    app.patients[patient_id] = patient_out
    return patient_out


# task 1.5
@app.get("/patient/{id}", status_code=200)
def get_patient(id: int):
    if id in app.patients:
        return app.patients.get(id)
    elif id < 1:
        return Response(status_code=400)
    else:
        return Response(status_code=404)


# task 3.1
@app.get("/hello", response_class=HTMLResponse)
def hello_function():
    today_date = date.today().strftime("%Y-%m-%d")
    return """<h1>Hello! Today date is {}</h1>""".format(today_date)
