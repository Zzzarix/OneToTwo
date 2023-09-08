import os
import pathlib


class TestFactory:
    service_name = "TEST_SERVICE"

    @classmethod
    def get_config_path(cls) -> str:
        path = pathlib.Path(__file__)
        return os.path.join(path.parent.parent, "configs", "test_config.yml")
