from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/")
async def put_root(payload: dict):
    return {"body": "Processed payload {}".format(payload)}