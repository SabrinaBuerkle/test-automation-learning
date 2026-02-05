import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

def get_logger(name):
    return logging.getLogger(name)