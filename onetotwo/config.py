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


class AppLoggerConfig(BaseConfig):
    """Config for app logger"""

    _name = "applog"
    log_format: str
    handlers: Dict[str, Any]
    level: str


class CacheConfig(BaseConfig):
    """Config for app cache"""

    _name = "cache"


class TarantoolConfig(BaseConfig):
    """Config for app logger"""

    _name = "tarantool"
    host: str
    port: int
    user: str
    password: str


# %% Manager
class ConfigManager:
    """Config manager"""

    app: AppConfig
    applog: AppLoggerConfig
    # cache_config: CacheConfig
    tarantool: TarantoolConfig

    @classmethod
    def load_config(cls, path: str) -> None:
        with open(path, "r") as f:
            config: Dict[str, Any] = yaml_load(f)

            config_classes = inspect.get_annotations(cls)

            for k in config.keys():
                setattr(cls, k, config_classes[k](**config[k]))
