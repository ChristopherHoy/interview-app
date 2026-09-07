from fastapi import FastAPI, Request
import uvicorn
from time import sleep
from pydantic import BaseModel

app = FastAPI()


class APIResponse(BaseModel):
    status: str


@app.post("/process")
async def read_item(request: Request) -> APIResponse:
    await request.json()
    sleep(1)
    
    return APIResponse(
        status="SUCCESS"
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8092, reload=True)