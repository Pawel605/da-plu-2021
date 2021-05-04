from fastapi import FastAPI, Request, Response
from pydantic import BaseModel


app = FastAPI()
app.counter = 0


class HelloResp(BaseModel):
    msg: str
