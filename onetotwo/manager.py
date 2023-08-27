# %% Import dependencies
from abc import ABC
from datetime import datetime
from typing import Generic, TypeVar
import uuid
import firebase_admin as firebase
from firebase_admin import db

from onetotwo.model import FireBaseModel


T = TypeVar("T", FireBaseModel)

# %% Models
class FireBaseManager(Generic[T], ABC):
    """Base manager for FireBaseModels"""

    def __init__(self, app_name: str, model_name: str) -> None:
        """Init FireBaseManager"""
        self._app: firebase.App = firebase.get_app(app_name)
        self._ref = db.reference(f"/{model_name}/", app=self._app)
    
    def create(self, **kwargs) -> T:
        """Create model"""

        kwargs["uid"] = uuid.uuid4()
        kwargs["created_at"] = datetime.utcnow()

        model: FireBaseModel = T(**kwargs)

        self._ref.child(model.uid).set(model.to_json())

        return model
