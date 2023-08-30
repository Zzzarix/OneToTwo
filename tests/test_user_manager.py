import pytest
from onetotwo.applogger import AppLogger
from onetotwo.config import AppLoggerConfig
from onetotwo.user.manager import UserManager
from onetotwo.user.model import User, UserLocale
from tests.factory import TestFactory

TestFactory.init_firebase_app()


class TestUserManager:
    @pytest.fixture()
    def app_name(self) -> str:
        return TestFactory.app_name

    @pytest.fixture()
    def logger(self) -> AppLogger:
        return AppLogger(
            "OneWay",
            AppLoggerConfig(
                level="DEBUG",
                log_format="%(asctime)s %(service_name)s %(env_type)s %(levelname)s: %(message)s",
                handlers={"stream": {"handler": "stdout"}},
            ),
        )

    def test_init(self, app_name: str, logger: AppLogger):
        UserManager(app_name=app_name, logger=logger, model=User)

    def test_create(self, app_name: str, logger: AppLogger):
        manager = UserManager(app_name=app_name, logger=logger, model=User)

        user = manager.create("User", "user@user.com", "userpwd", UserLocale.Rus)

        assert user.name == "User"
        assert user.email == "user@user.com"
        assert user.password == "userpwd"
        assert user.locale == UserLocale.Rus
