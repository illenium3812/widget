from fastapi import FastAPI
from uberall import Uberall

app = FastAPI()




@app.get("/")
async def home():
    return "Waiting for the query"


@app.get("/{query}")
async def get_results(query):
    uberall = Uberall()
    return uberall.make_call(query)
