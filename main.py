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


# task 3.1
@app.get("/hello", response_class=HTMLResponse)
def hello_function():
    today_date = date.today().strftime("%Y-%m-%d")
    return """<h1>Hello! Today date is {}</h1>""".format(today_date)
