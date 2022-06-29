from fastapi import FastAPI
from uberall import Uberall

app = FastAPI()

uberall = Uberall()


@app.get("/")
async def home():
    return "Waiting for the query"


@app.get("/{query}")
async def get_results(query):
    return uberall.make_call(query)
