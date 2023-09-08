# %% Import dependencies
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from onetotwo.model import ImmutableModel, MutableModel


# %% Enums
class WayLifetime(int, Enum):
    Permanent = 0
    Day = 1
    ThreeDays = 3
    Week = 7
    Month = 30


# %% Models
class TargetUrl(MutableModel):
    """Target url model"""

    is_secured: bool
    domain: str
    path: str
    params: Dict[str, str]

    def format(self) -> str:
        return self.domain + self.path + "?" + "&".join([k + "=" + v for k, v in self.params.items()])


class OneWay(MutableModel):
    """Shortened link model"""

    uid: str
    name: str
    target: TargetUrl
    alias: str
    is_temporary: bool
    lifetime: WayLifetime
    user_uid: Optional[str]
    created_at: datetime


class Redirect(ImmutableModel):
    """Redirect model"""

    uid: str
    ip: str
    oneway_uid: str
    created_at: datetime
