import logging
from app.core.config import settings
from opencensus.ext.azure.log_exporter import AzureLogHandler


class LoggerConfigurator:
    @staticmethod
    def configure_logger(name: str):
        """
        Configure and return a logger with the given name.

        Args:
            name (str): Namespace of caller (__name__)

        Returns:
            logger (Logger): Logger configured to caller's namespace and handler.

        Example usage within other modules:
            from app.core.logging import LoggerConfigurator
            logger = LoggerConfigurator.configure_logger(__name__)
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Check if the logger already has handlers to avoid duplicates
        if not logger.handlers:
            if settings.LOG_APPINSIGHTS:
                app_insights_handler = AzureLogHandler(connection_string=settings.APPLICATIONINSIGHTS_CONNECTION_STRING)
                logger.addHandler(app_insights_handler)
            else:
                console_handler = logging.StreamHandler()
                logger.addHandler(console_handler)

        return logger


logger = LoggerConfigurator.configure_logger
