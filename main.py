from hashlib import sha256

from fastapi import FastAPI, Response, status, Depends, Request, Query, Cookie, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
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
app.session_token = []
app.token = []


@app.post("/login_session", status_code=status.HTTP_201_CREATED)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = compare_digest(credentials.username, username)
    correct_password = compare_digest(credentials.password, password)

    if correct_username and correct_password:
        session_token = sha256(f"{username}{password}{app.session_secret_key}".encode()).hexdigest()
        if len(app.session_token) == 3:
            app.session_token.pop(0)
        app.session_token.append(session_token)
        response.set_cookie(key="session_token", value=session_token)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.post("/login_token", status_code=status.HTTP_201_CREATED)
def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = compare_digest(credentials.username, username)
    correct_password = compare_digest(credentials.password, password)
    if correct_username and correct_password:
        token_value = sha256(f"{username}{password}{app.token_secret_key}".encode()).hexdigest()
        if len(app.token) == 3:
            app.token.pop(0)
        app.token.append(token_value)
        return {"token": token_value}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


# task 3.3
@app.get("/welcome_session", status_code=status.HTTP_200_OK)
def welcome_session(session_token: str = Cookie(None), format: str = ""):
    if (session_token not in app.session_token) or (session_token == ""):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised")
    if format == "json":
        return {"message": "Welcome!"}
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return PlainTextResponse(content="Welcome!")


@app.get("/welcome_token", status_code=status.HTTP_200_OK)
def welcome_token(token: str, format: str = ""):
    if (token not in app.token) or (token == ""):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised")
    if format == "json":
        return {"message": "Welcome!"}
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return PlainTextResponse(content="Welcome!")


# task 3.4


@app.delete("/logout_session")
def logout_session(format: str = "", session_token: str = Cookie(None)):
    if session_token not in app.session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    app.session_token.remove(session_token)
    url = "/logged_out?format=" + format
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.delete("/logout_token")
def logout_token(format: str = "", token: str = ""):
    if token == "" or token not in app.token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    app.token.remove(token)
    url = "/logged_out?format=" + format
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


# task 3.5
@app.get("/logged_out")
def logged_out(format: str = ""):
    if format == "json":
        return {"message": "Logged out!"}
    elif format == "html":
        return HTMLResponse(content="<h1>Logged out!</h1>", status_code=status.HTTP_200_OK)
    else:
        return PlainTextResponse(content="Logged out!", status_code=status.HTTP_200_OK)
