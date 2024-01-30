import logging
from app.core.config import settings
from opencensus.ext.azure.log_exporter import AzureLogHandler

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if settings.LOG_APPINSIGHTS:        
    ai_handler = AzureLogHandler(connection_string=f'InstrumentationKey={settings.APPINSIGHTS_INSTRUMENTATIONKEY}')
    logger.addHandler(ai_handler)
else:
    # Print logs to the console
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)