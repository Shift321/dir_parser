import logging
import sys
from typing import Optional


class CustomLogging:
    def __init__(self, log_path, verbose):
        self.log_path = log_path
        self.verbose = verbose
        if self.verbose:
            handlers = [logging.FileHandler(self.log_path), logging.StreamHandler(sys.stdout)]
        else:
            handlers = [logging.FileHandler(self.log_path)]
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",
                            handlers=handlers)

    @staticmethod
    def write_logs(msg, level: Optional[str] = None):
        if level == "Error":
            logging.error(msg)
        else:
            logging.info(msg)

    @staticmethod
    def finish_logs():
        logging.info("Script finished")
