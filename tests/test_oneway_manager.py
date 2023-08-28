import pytest
from onetotwo.oneway.manager import OneWayManager, RedirectManager
from onetotwo.oneway.model import OneWay, Redirect, WayLifetime
from tests.factory import TestFactory

TestFactory.init_firebase_app()


class TestOneWayManager:
    @pytest.fixture()
    def app_name(self) -> str:
        return TestFactory.app_name

    @pytest.fixture()
    def redirect_manager(self, app_name: str) -> RedirectManager:
        return RedirectManager(app_name, model=Redirect)

    def test_init(self, app_name: str, redirect_manager: RedirectManager):
        OneWayManager(app_name=app_name, model=OneWay, redirect_manager=redirect_manager)

    def test_create(self, app_name: str, redirect_manager: RedirectManager):
        manager = OneWayManager(app_name=app_name, model=OneWay, redirect_manager=redirect_manager)

        way = manager.create(
            "Way",
            "adfh",
            "https://google.com/query/search?param1=val1&param2=val2",
            is_temporary=True,
            lifetime=WayLifetime.Day,
            user_uid=None,
        )

        assert way.name == "Way"
        assert way.target.domain == "google.com"
        assert way.target.params == {"param1": "val1", "param2": "val2"}
