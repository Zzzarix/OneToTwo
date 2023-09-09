# %% Import Dependencies
from typing import Optional, Type

from onetotwo.applogger import AppLogger
from onetotwo.manager import MongoManager
from onetotwo.user.model import User, UserLocale


# %% Manager
class UserManager(MongoManager[User]):
    """User mongodb manager"""

    @classmethod
    def init(cls, logger: AppLogger, model: Type[User]) -> None:
        super().init(logger, model)

    @classmethod
    def create(cls, name: str, email: str, password: str, locale: UserLocale) -> User:
        """Create User model"""
        return cls._create(name=name, email=email, password=password, locale=locale, is_active=True)

    @classmethod
    def get(cls, uid: str) -> Optional[User]:
        """Get user model"""
        return cls._get_one({"_id": uid})

    @classmethod
    def delete(cls, uid: str) -> None:
        """Delete user model"""
        cls._delete({"_id": uid})
