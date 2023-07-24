from fastapi import FastAPI
from controller.claude_apis import router


def register_api_routers(app: FastAPI):
    app.include_router(router)
    return app
