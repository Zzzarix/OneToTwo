import os
import pathlib

import firebase_admin as firebase


class TestFactory:
    app_name = "TEST_NAME"

    _app_inited = False

    @classmethod
    def init_firebase_app(cls):
        if cls._app_inited:
            return
        path = pathlib.Path(__file__)
        credential = firebase.credentials.Certificate(os.path.join(path.parent.parent, "secrets", "firebase_key.json"))
        firebase.initialize_app(
            credential=credential,
            options={"databaseURL": "https://onetotwo-2c516-default-rtdb.firebaseio.com/"},
            name=cls.app_name,
        )
        cls._app_inited = True
