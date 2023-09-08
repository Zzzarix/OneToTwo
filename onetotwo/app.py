from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from onetotwo.api import router
from onetotwo.config import ConfigManager
from uvicorn import run

app = FastAPI(debug=ConfigManager.app.debug)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(router)


@app.on_event("startup")
def startup():
    pass


if __name__ == "__main__":
    run("app:app", host=ConfigManager.app.host, port=ConfigManager.app.port, reload=True)
