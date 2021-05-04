from hashlib import sha256

from fastapi import FastAPI, Response, status, Depends, Request, Query, Cookie, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from datetime import date
from secrets import compare_digest

app = FastAPI()
app.counter = 0
security = HTTPBasic()


class HelloResp(BaseModel):
    msg: str


# task 3.1
@app.get("/hello", response_class=HTMLResponse)
def hello_function():
    today_date = date.today().strftime("%Y-%m-%d")
    return """<h1>Hello! Today date is {}</h1>""".format(today_date)


# task 3.2

username = "4dm1n"
password = "NotSoSecurePa$$"
app.session_secret_key = "very constant and random secret, best 64+ characters"
app.token_secret_key = "another very constant and random secret with random numbers 3985020104"
app.session_token = None
app.token = None


@app.post("/login_session", status_code=status.HTTP_201_CREATED)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = compare_digest(credentials.username, username)
    correct_password = compare_digest(credentials.password, password)

    if correct_username and correct_password:
        session_token = sha256(f"{username}{password}{app.session_secret_key}".encode()).hexdigest()
        app.session_token = session_token
        response.set_cookie(key="session_token", value=session_token)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.post("/login_token", status_code=status.HTTP_201_CREATED)
def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = compare_digest(credentials.username, username)
    correct_password = compare_digest(credentials.password, password)
    if correct_username and correct_password:
        token_value = sha256(f"{username}{password}{app.token_secret_key}".encode()).hexdigest()
        app.token = token_value
        return {"token": token_value}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

# task 3.3