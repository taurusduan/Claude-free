from fastapi import FastAPI
import uvicorn

from controller.api_router import register_api_routers

app = FastAPI()
register_api_routers(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
