# %% Import dependencies
import uuid
from abc import ABC
from datetime import datetime
from typing import Generic, TypeVar

import firebase_admin as firebase
from firebase_admin import db

T = TypeVar("T")


# %% Manager
class FireBaseManager(Generic[T], ABC):
    """Base manager for FireBaseModels"""

    def __init__(self, app_name: str, model_name: str) -> None:
        """Init FireBaseManager"""
        self._app: firebase.App = firebase.get_app(app_name)
        self._ref = db.reference(f"/{model_name}/", app=self._app)

    def _create(self, **kwargs) -> T:
        """Create model"""

        kwargs["uid"] = uuid.uuid4()
        kwargs["created_at"] = datetime.utcnow()

        model = T(**kwargs)

        self._ref.child(model.uid).set(model.to_json())

        return model

    def _get(self, uid: str) -> T:
        """Get model"""
        res = self._ref.child(uid).get()

        return T(**res)

    def _update(self, uid: str, **kwargs) -> None:
        """Update model"""
        self._ref.child(uid).update(kwargs)

    def _delete(self, uid: str) -> None:
        """Delete model"""
        self._ref.child(uid).delete()
