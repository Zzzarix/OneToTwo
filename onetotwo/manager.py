# %% Import dependencies
from abc import ABC
from datetime import datetime
from typing import Generic, Type, TypeVar

import firebase_admin as firebase
from firebase_admin import db
from onetotwo.applogger import AppLogger
from onetotwo.utils import make_uuid

T = TypeVar("T")


# %% Manager
class FireBaseManager(Generic[T], ABC):
    """Base manager for FireBaseModels"""

    def __init__(self, app_name: str, logger: AppLogger, model: Type[T]) -> None:
        """Init FireBaseManager"""
        self._app: firebase.App = firebase.get_app(app_name)
        self._ref = db.reference(f"/{model.__name__}/", app=self._app)
        self._logger = logger
        self._model = model

    def _create(self, **kwargs) -> T:
        """Create model"""

        kwargs["uid"] = make_uuid()
        kwargs["created_at"] = datetime.utcnow()

        model = self._model(**kwargs)

        self._ref.child(model.uid).set(model.to_json())

        return model

    def _get(self, uid: str) -> T:
        """Get model"""
        res = self._ref.child(uid).get()

        return self._model(**res)

    def _update(self, uid: str, **kwargs) -> None:
        """Update model"""
        self._ref.child(uid).update(kwargs)

    def _delete(self, uid: str) -> None:
        """Delete model"""
        self._ref.child(uid).delete()
