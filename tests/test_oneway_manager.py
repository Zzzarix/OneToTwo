import pytest
from onetotwo.applogger import AppLogger
from onetotwo.config import AppLoggerConfig
from onetotwo.oneway.manager import OneWayManager, RedirectManager
from onetotwo.oneway.model import OneWay, Redirect, WayLifetime
from tests.factory import TestFactory


TestFactory.init_firebase_app()

def pytest_namespace():
    return {'shared': None}

class TestOneWayManager:
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

    @pytest.fixture()
    def redirect_manager(self, app_name: str, logger: AppLogger) -> RedirectManager:
        return RedirectManager(app_name=app_name, logger=logger, model=Redirect)

    def test_init(self, app_name: str, logger: AppLogger, redirect_manager: RedirectManager):
        OneWayManager(app_name=app_name, logger=logger, model=OneWay, redirect_manager=redirect_manager)

    def test_create(self, app_name: str, logger: AppLogger, redirect_manager: RedirectManager):
        manager = OneWayManager(app_name=app_name, logger=logger, model=OneWay, redirect_manager=redirect_manager)

        way = manager.create(
            "Way",
            "https://google.com/query/search?param1=val1&param2=val2",
            is_temporary=True,
            lifetime=WayLifetime.Day,
            user_uid=None,
        )

        pytest.shared = way

        assert way.name == "Way"
        assert way.target.domain == "google.com"
        assert way.target.params == {"param1": "val1", "param2": "val2"}

    def test_redirect(self, app_name: str, redirect_manager: RedirectManager):
        manager = OneWayManager(app_name=app_name, model=OneWay, redirect_manager=redirect_manager)
        print(pytest.shared.alias)
        res = manager.redirect(pytest.shared.alias, "127.0.0.1")

        assert res
        assert res == pytest.shared.target.format()

        redirects = redirect_manager.get_redirects(pytest.shared.uid)

        assert len(redirects) == 1

        assert redirects[0].ip == "127.0.0.1"
