# %% Import dependencies
from abc import ABC

from pydantic import BaseModel


# %% Base models
class TarantoolModel(BaseModel, ABC):
    """Model for storing in Tarantool"""

    model_config = {"extra": "ignore"}

    def to_json(self) -> str:
        """Return json representation of model"""
        return self.model_dump_json(by_alias=True)


class MutableModel(TarantoolModel, ABC):
    """Mutable model"""

    model_config = {
        "frozen": False,
    }


class ImmutableModel(TarantoolModel, ABC):
    """Immutable model"""

    model_config = {
        "frozen": True,
    }


class BaseConfig(ImmutableModel, ABC):
    """Base config model"""

    _name: str

    model_config = {
        "ignored_types": (
            str,
            int,
        )
    }
