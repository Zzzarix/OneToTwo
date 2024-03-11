# %% Import dependencies
from enum import Enum
from typing import Dict, Optional

from bitter.model import MongoModel, ObjectModel


# %% Enums
class WayLifetime(int, Enum):
    Permanent = 0
    Day = 24
    ThreeDays = 72
    Week = 168
    # Month = 30


# %% Models
class TargetUrl(ObjectModel):
    """Target url model"""

    is_secured: bool
    domain: str
    path: str
    params: Dict[str, str]

    def to_str(self) -> str:
        schema = "https://" if self.is_secured else "http://"
        params = "&".join([k + "=" + v for k, v in self.params.items()])
        query = ("?" + params) if params else ""
        return schema + self.domain + self.path + query


class OneWay(MongoModel):
    """Shortened link model"""

    _collection_name = "oneways"

    target: TargetUrl
    alias: str
    is_temporary: bool
    lifetime: WayLifetime
    user_uid: Optional[str]


class Redirect(MongoModel):
    """Redirect model"""

    _collection_name = "redirects"

    ip: Optional[str]
    oneway_uid: str
