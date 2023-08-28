import pytest

from onetotwo.manager import FireBaseManager
from onetotwo.model import FireBaseModel

class TestFireBaseManager:
    
    def test_init(self, app_name: str):
        manager = FireBaseManager(app_name=app_name, model=FireBaseModel)
