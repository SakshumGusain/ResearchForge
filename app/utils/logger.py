import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(filename='logs/app.log', filemode='a', format='%(asctime)s | %(levelname)s | %(name)s | %(message)s', level=logging.DEBUG)

stream_logger = logging.StreamHandler()
stream_logger.setLevel(logging.INFO)

def get_logger(module_name):
    logger = logging.getLogger(module_name)
    if not logger.handlers:
        logger.addHandler(stream_logger)
    return logger