# %% Import Dependencies
from typing import Type

from onetotwo.applogger import AppLogger
from onetotwo.manager import FireBaseManager
from onetotwo.user.model import User, UserLocale


# %% Manager
class UserManager(FireBaseManager[User]):
    """User firebase manager"""

    def __init__(self, app_name: str, logger: AppLogger, model: Type[User]) -> None:
        super().__init__(app_name, logger, model)

    def create(self, name: str, email: str, password: str, locale: UserLocale) -> User:
        """Create User model"""
        return self._create(name=name, email=email, password=password, locale=locale, is_active=True)

    def get(self, uid: str) -> User:
        """Get user model"""
        return self._get(uid)

    def delete(self, uid: str) -> None:
        """Delete user model"""
        self._delete(uid)
