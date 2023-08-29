import os
import pathlib

import firebase_admin as firebase
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from onetotwo.api import router
from uvicorn import run

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(router)


@app.on_event("startup")
def startup():
    path = pathlib.Path(__file__)
    credential = firebase.credentials.Certificate(os.path.join(path.parent.parent, "secrets", "firebase_key.json"))
    firebase.initialize_app(
        credential=credential,
        options={"databaseURL": "https://onetotwo-2c516-default-rtdb.firebaseio.com/"},
        name="TEST_APP",
    )


if __name__ == "__main__":
    run("app:app", reload=True)
