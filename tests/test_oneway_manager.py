import pytest
from onetotwo.applogger import AppLogger
from onetotwo.config import AppLoggerConfig
from onetotwo.oneway.manager import OneWayManager, RedirectManager
from onetotwo.oneway.model import OneWay, Redirect, WayLifetime


def pytest_namespace():
    return {"shared": None}


class TestOneWayManager:
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

    # @pytest.fixture()
    # def redirect_manager(self, logger: AppLogger) -> RedirectManager:
    #     return RedirectManager(logger=logger, model=Redirect)

    def test_init(self, logger: AppLogger):
        OneWayManager.init(logger=logger, model=OneWay)

    def test_create(self, logger: AppLogger):
        OneWayManager.init(logger=logger, model=OneWay)

        way = OneWayManager.create(
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

    def test_redirect(self, logger: AppLogger):
        RedirectManager.init(logger=logger, model=Redirect)
        OneWayManager.init(logger=logger, model=OneWay)
        res = OneWayManager.redirect(pytest.shared.alias, "127.0.0.1")

        assert res
        assert res == pytest.shared.target.to_str()

        redirects = RedirectManager.get_redirects(pytest.shared.uid)

        assert len(redirects) == 1

        assert redirects[0].ip == "127.0.0.1"
