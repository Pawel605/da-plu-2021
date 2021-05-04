from fastapi import FastAPI, Response, Request, Query, Cookie, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from datetime import date

app = FastAPI()
app.counter = 0


class HelloResp(BaseModel):
    msg: str


# task 3.1
@app.get("/hello", response_class=HTMLResponse)
def hello_function():
    today_date = date.today().strftime("%Y-%m-%d")
    return """<h1>Hello! Today date is {}</h1>""".format(today_date)
