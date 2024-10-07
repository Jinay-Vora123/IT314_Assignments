import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Logger:
    @staticmethod
    def log_info(message: str):
        logging.info(message)

    @staticmethod
    def log_debug(message: str):
        logging.debug(message)

    @staticmethod
    def log_error(message: str):
        logging.error(message)
