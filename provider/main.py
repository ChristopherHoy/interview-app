from fastapi import FastAPI, Request
import uvicorn
from time import sleep

app = FastAPI()


@app.post("/process")
async def read_item(request: Request):
    await request.json()
    sleep(1)
    return {
        "status": "success"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8092, reload=True)