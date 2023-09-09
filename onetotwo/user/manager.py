# %% Import Dependencies
from typing import Optional, Type

from onetotwo.applogger import AppLogger
from onetotwo.manager import MongoManager
from onetotwo.user.model import User, UserLocale


# %% Manager
class UserManager(MongoManager[User]):
    """User mongo manager"""

    def __init__(self, logger: AppLogger, model: Type[User]) -> None:
        super().__init__(logger, model)

    def create(self, name: str, email: str, password: str, locale: UserLocale) -> User:
        """Create User model"""
        return self._create(name=name, email=email, password=password, locale=locale, is_active=True)

    def get(self, uid: str) -> Optional[User]:
        """Get user model"""
        return self._get_one({"_id": uid})

    def delete(self, uid: str) -> None:
        """Delete user model"""
        self._delete({"_id": uid})
