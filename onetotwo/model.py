# %% Import dependencies
from abc import ABC

from pydantic import BaseModel


# %% Base models
class FireBaseModel(BaseModel, ABC):
    """Model for storing in Firebase"""

    uid: str

    model_config = {"extra": "ignore"}

    def to_json(self) -> str:
        """Return json representation of model"""
        return self.model_dump_json(by_alias=True)


class MutableModel(FireBaseModel, ABC):
    """Mutable model"""

    model_config = {
        "frozen": False,
    }


class ImmutableModel(FireBaseModel, ABC):
    """Immutable model"""

    model_config = {
        "frozen": True,
    }
