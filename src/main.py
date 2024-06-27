from fastapi import FastAPI

app = FastAPI()


@app.get("/status")
def status():
    return {"status_code": 200}
