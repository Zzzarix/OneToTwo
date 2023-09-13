import pytest
from bitter.applogger import AppLogger
from bitter.config import AppLoggerConfig
from tests.factory import TestFactory


class TestAppLogger:
    @pytest.fixture()
    def config(self) -> AppLoggerConfig:
        return AppLoggerConfig(
            level="DEBUG",
            log_format="%(asctime)s %(service_name)s %(env_type)s %(levelname)s: %(message)s",
            handlers={"stream": {"handler": "stdout"}},
        )

    def test_init(self, config: AppLoggerConfig) -> None:
        logger = AppLogger(TestFactory.service_name, config=config)

        assert isinstance(logger, AppLogger)
        assert logger._logger.name == TestFactory.service_name
        assert logger._config == config

    def test_log(self, config: AppLoggerConfig) -> None:
        logger = AppLogger(TestFactory.service_name, config=config)

        logger.debug("Test debug")
        logger.info("Test info")
        logger.warning("Test warning")

        logger.error(ValueError("Test error"))
        try:
            x = 1 / 0
        except ZeroDivisionError as ex:
            logger.error(ex, "Test error")

        logger.critical(RuntimeError("Test critical"))
        logger.critical(NotImplementedError("Test critical"), "Critical message")
