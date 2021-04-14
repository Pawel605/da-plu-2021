from fastapi import FastAPI

app = FastAPI()
app.counter = 0

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def hello_name_view(name: str):
    return f"Hello {name}"

@app.get('/counter')
def counter():
    app.counter += 1
    return app.counter