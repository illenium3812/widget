from fastapi import FastAPI
from uberall import Uberall

app = FastAPI()

uberall = Uberall()


@app.get("/{query}")
async def get_results(query):
    return uberall.make_call(query)


@app.get("/test/")
async def test():
    return {
        'id': 'hello',
        'name': 'test'
    }
