import os
import pathlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bitter.api import router
from bitter.applogger import AppLogger
from bitter.config import ConfigManager
from bitter.oneway.manager import OneWayManager, RedirectManager
from bitter.oneway.model import OneWay, Redirect
from bitter.user.manager import UserManager
from bitter.user.model import User
from uvicorn import run

fpath = pathlib.Path(__file__)
path = os.path.join(fpath.parent.parent, "configs", "config.yml")
ConfigManager.load_config(path)

app = FastAPI(
    debug=ConfigManager.app.debug,
    title="Bitter",
    version=ConfigManager.app.version,
    openapi_url=f"/api/{ConfigManager.app.api_version}/openapi.json",
    docs_url=f"/api/{ConfigManager.app.api_version}/docs",
)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(router)


@app.on_event("startup")
def startup():
    """Startup function"""

    user_logger = AppLogger("User", ConfigManager.applog)
    UserManager.init(user_logger, User)

    redirect_logger = AppLogger("Redirect", ConfigManager.applog)
    RedirectManager.init(redirect_logger, Redirect)

    way_logger = AppLogger("OneWay", ConfigManager.applog)
    OneWayManager.init(way_logger, OneWay)


if __name__ == "__main__":
    run("app:app", host=ConfigManager.app.host, port=ConfigManager.app.port, reload=True)
