# %% Import dependencies
from datetime import datetime
from enum import Enum

from onetotwo.model import MutableModel


# %% Enums
class UserLocale(Enum, str):
    Rus = "ru"
    Eng = "en"


# %% Models
class User(MutableModel):
    """User model"""

    name: str
    email: str
    password: str
    locale: UserLocale
    created_at: datetime
    is_active: bool
