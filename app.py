from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.post("/signup")
async def signup():
    return {"message": "Signup successful"}


@app.post("/signin")
async def signin():
    return {"message": "Signin successful"}


handler = Mangum(app)
