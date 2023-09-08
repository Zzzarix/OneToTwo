# %% Import dependencies
from abc import ABC

from pydantic import BaseModel


# %% Base models
class TarantoolModel(BaseModel, ABC):
    """Model for storing in Tarantool"""

    model_config = {"extra": "ignore"}

    @classmethod
    def from_tuple(cls, data: tuple) -> "TarantoolModel":
        """Return model from tuple representation"""
        return cls.model_validate(data)

    def to_tuple(self) -> tuple:
        """Return tuple representation of model"""
        return tuple(self.model_dump(mode="json", by_alias=True).values())


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
