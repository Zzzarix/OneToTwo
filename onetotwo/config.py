# %% Import dependency
import inspect
from typing import Any, Dict

from onetotwo.model import BaseConfig
from yaml import full_load as yaml_load


# %% Models
class AppConfig(BaseConfig):
    """Config for FastAPI app"""

    _name = "app"
    debug: bool
    host: str
    port: int


class LogConfig(BaseConfig):
    """Config for app logger"""

    _name = "log"


class CacheConfig(BaseConfig):
    """Config for app cache"""

    _name = "cache"


# %% Manager
class ConfigManager:
    """Config manager"""

    app: AppConfig
    # log_config: LogConfig
    # cache_config: CacheConfig

    @classmethod
    def load_config(cls, path: str) -> None:
        with open(path, "r") as f:
            config: Dict[str, Any] = yaml_load(f)

            config_classes = inspect.get_annotations(cls)

            for k in config.keys():
                setattr(cls, k, config_classes[k](**config[k]))
