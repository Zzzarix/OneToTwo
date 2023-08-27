# %% Import dependencies
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from onetotwo.model import MutableModel


# %% Enums
class LinkLifetime(Enum, int):
    Permanent = 0
    Day = 1
    ThreeDays = 3
    Week = 7


# %% Models
class TargetUrl(MutableModel):
    """Target url model"""

    is_secured: bool
    domain: str
    path: str
    params: Dict[str, Any]


class Link(MutableModel):
    """Shorted link model"""

    name: str
    target: TargetUrl
    is_temporary: bool
    lifetime: LinkLifetime
    user_uid: Optional[str]
    created_at: datetime


class Redirect(MutableModel):
    """Redirect model"""

    ip: str
    link_uid: str
    created_at: datetime
