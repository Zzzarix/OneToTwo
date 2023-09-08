# %% Import dependencies
from abc import ABC
from datetime import datetime
from typing import Generic, TypeVar

import tarantool
from onetotwo.config import ConfigManager
from onetotwo.applogger import AppLogger
from onetotwo.model import TarantoolModel

T = TypeVar("T", bound=TarantoolModel)


# %% Manager
class TarantoolManager(Generic[T], ABC):
    """Base manager for TarantoolModels"""

    def __init__(self, space_name: str, logger: AppLogger) -> None:
        """Init TarantoolManager"""
        self._conn: tarantool.Connection = self.__init()
        self._space = self._conn.space(space_name)
        self._logger = logger

    def __init(self) -> tarantool.Connection:
        """Init Tarantool connection"""

        connection: tarantool.Connection = tarantool.connect(
            host=ConfigManager.tarantool.host,
            port=ConfigManager.tarantool.port,
            user=ConfigManager.tarantool.user,
            password=ConfigManager.tarantool.password
        )

        return connection


    def __create_model(self, model: T) -> None:
        """Create model"""

        self._space.insert(model.to_tuple())

    def __find_models(self, uid: str) -> IterableT:
        """Find models"""
        self._space.select()

        return self._model(**res)

    def __update_model(self, uid: str, **kwargs) -> None:
        """Update model"""
        self._ref.child(uid).update(kwargs)

    def __delete_model(self, uid: str) -> None:
        """Delete model"""
        self._ref.child(uid).delete()
