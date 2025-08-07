import logging
import sys
from pythonjsonlogger import jsonlogger

LOG_LEVEL = "INFO"

def setup_logger():
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    log_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    root_logger.addHandler(log_handler)

    # Optional: silence overly noisy loggers
    logging.getLogger("uvicorn.access").setLevel("WARNING")
    logging.getLogger("uvicorn.error").setLevel("INFO")
    logging.getLogger("sqlalchemy.engine").setLevel("WARNING")

# Call this early in your main.py or app startup
setup_logger()

# Use this everywhere in the app
logger = logging.getLogger("orbank")
