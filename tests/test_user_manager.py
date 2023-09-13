import pytest
from bitter.applogger import AppLogger
from bitter.config import AppLoggerConfig
from bitter.user.manager import UserManager
from bitter.user.model import User, UserLocale


class TestUserManager:
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

    def test_init(self, logger: AppLogger):
        UserManager.init(logger=logger, model=User)

    def test_create(self, logger: AppLogger):
        UserManager.init(logger=logger, model=User)

        user = UserManager.create("User", "user@user.com", "userpwd", UserLocale.Rus)

        assert user.name == "User"
        assert user.email == "user@user.com"
        assert user.password == "userpwd"
        assert user.locale == UserLocale.Rus
