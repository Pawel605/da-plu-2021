from fastapi import FastAPI, Response, Request, Query, Cookie, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi_mako import FastAPIMako
from fastapi.templating import Jinja2Templates
from routers.router import router
from hashlib import sha256
from secrets import compare_digest
from datetime import date
from fastapi.security import HTTPBasicCredentials, HTTPBasic


app = FastAPI()
app.counter = 0
security = HTTPBasic()


class HelloResp(BaseModel):
    msg: str


# example 1

@app.get("/request_query_string_discovery_1/")
def read_item(request: Request):
    print(f"{request.query_params=}")
    return request.query_params


# example 2

@app.get("/request_query_string_discovery_2/")
def read_items(u: str = Query("default"), q: List[str] = Query(None)):
    query_items = {"q": q, "u": u}
    return query_items


# example 3 - static HTML

@app.get("/static", response_class=HTMLResponse)
def index_static():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look me! HTML!</h1>
        </body>
    </html>
    """


# example 4 - Jinja
templates = Jinja2Templates(directory="templates")


@app.get("/jinja")
def read_item(request: Request):
    return templates.TemplateResponse("index.html.j2", {
        "request": request, "my_string": "Wheeeee!", "my_list": [0, 1, 2, 3, 4, 5]})


# example 5 - mako

app.__name__ = "templates"
mako = FastAPIMako(app)


@app.get("/mako", response_class=HTMLResponse)
@mako.template("index_mako.html")
def index_mako(request: Request):
    setattr(request, "mako", "test")
    return {"my_string": "Wheeeee!", "my_list": [0, 1, 2, 3, 4, 5]}


# example 6 - routing static and dynamic

@app.get("/hello/")
def hello():
    return {"hello_world": "hello_world"}


@app.get("/simple_path_tmpl/{sample_variable}")
def simple_path_tmpl(sample_variable: str):
    print(f"{sample_variable=}")
    print(type(sample_variable))
    return {"sample_variable": sample_variable}


@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}


# example 7 router


app.include_router(
    router, prefix="/v1", tags=["api_v1"],
)

app.include_router(router, tags=["default"])


# example 8 - cookie

@app.get("/items/")
def read_items(*, ads_id: str = Cookie(None)):
    return {"ads_id": ads_id}


@app.post("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}


# example 9

app.secret_key = "very constant and random secret, best 64+ characters"
app.access_tokens = []


@app.post("/login/")
def login(user: str, password: str, response: Response):
    session_token = sha256(f"{user}{password}{app.secret_key}".encode()).hexdigest()
    app.access_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    return {"message": "Welcome"}


# example 10

@app.get("/data/")
def secured_data(*, response: Response, session_token: str = Cookie(None)):
    print(session_token)
    print(app.access_tokens)
    print(session_token in app.access_tokens)
    if session_token not in app.access_tokens:
        raise HTTPException(status_code=403, detail="Unathorised")
    else:
        return {"message": "Secure Content"}


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

