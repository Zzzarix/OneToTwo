# %% Import dependencies
from abc import ABC
from datetime import datetime
from typing import Any, Generic, Iterable, Optional, Type, TypeVar

import pymongo
from onetotwo.applogger import AppLogger
from onetotwo.config import ConfigManager
from onetotwo.model import MongoModel
from onetotwo.utils import make_uuid

T = TypeVar("T", bound=MongoModel)


# %% Manager
class MongoManager(Generic[T], ABC):
    """Base manager for MongoModels"""

    def __init__(self, logger: AppLogger, model: Type[T]) -> None:
        """Init MongoManager"""

        self._model = model

        self._client = pymongo.MongoClient(host=ConfigManager.mongo.uri)
        self._db = self._client.get_database(name=ConfigManager.mongo.database)
        self._collection = self._db.get_collection(self._model._collection_name)
        self._logger = logger

    def _create(self, **kwargs) -> T:
        """Create model"""

        kwargs["_id"] = make_uuid()
        kwargs["created_at"] = datetime.utcnow()

        model = self._model(**kwargs)

        self._collection.insert_one(model.to_dict())

        return model

    def _get_many(self, filt: dict[str, Any], limit: int = 0) -> Iterable[T]:
        """Find models"""

        res: list[T] = []
        for doc in self._collection.find(filt, limit=limit):
            res.append(self._model(**doc))
        return res

    def _get_one(self, filt: dict[str, Any]) -> Optional[T]:
        """Find model"""
        res = self._collection.find_one(filt)

        return self._model(**res) if res else None

    def _update(self, filt: dict[str, Any], update: dict[str, Any]) -> None:
        """Update models"""
        self._collection.update_many(filt, update)

    def _delete(self, filt: dict[str, Any]) -> None:
        """Delete models"""
        self._collection.delete_many(filt)
