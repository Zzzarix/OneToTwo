from onetotwo.config import ConfigManager
from tests.factory import TestFactory


class TestConfigManager:
    def test_load_config(self):
        path = TestFactory.get_config_path()

        ConfigManager.load_config(path)

        assert ConfigManager.app
        assert ConfigManager.app.debug == True
        assert ConfigManager.app.host == "127.0.0.1"
        assert ConfigManager.app.port == 8080
