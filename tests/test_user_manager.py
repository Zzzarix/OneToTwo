import pytest
from onetotwo.user.manager import UserManager
from onetotwo.user.model import User, UserLocale
from tests.factory import TestFactory

TestFactory.init_firebase_app()


class TestUserManager:
    @pytest.fixture()
    def app_name(self) -> str:
        return TestFactory.app_name

    def test_init(self, app_name: str):
        UserManager(app_name=app_name, model=User)

    def test_create(self, app_name: str):
        manager = UserManager(app_name=app_name, model=User)

        user = manager.create("User", "user@user.com", "userpwd", UserLocale.Rus)

        assert user.name == "User"
        assert user.email == "user@user.com"
        assert user.password == "userpwd"
        assert user.locale == UserLocale.Rus
