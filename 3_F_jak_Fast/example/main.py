from fastapi import FastAPI, Response, Request, Query, Cookie, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse
from hashlib import sha256
from fastapi_mako import FastAPIMako
from fastapi.templating import Jinja2Templates
from routers.router import router

app = FastAPI()
app.counter = 0


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
