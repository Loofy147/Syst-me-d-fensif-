import logging
from src.config import config

def setup_logging():
    log_level = config.get("logging", "level")
    log_file = config.get("logging", "log_file")

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ]
    )

    return logging.getLogger()

logger = setup_logging()
