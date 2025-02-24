# =====================================================================================================================
#                   Import
# =====================================================================================================================
import os
import re
import logging
from logging.handlers import TimedRotatingFileHandler


# =====================================================================================================================
#                   Environment Variable
# =====================================================================================================================
ENV_MODE = os.environ["MODE"]


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class LogFile:
    def __init__(self, name: str):
        current_work_dir = os.getcwd()
        log_dir = f"{current_work_dir}/../logs/{name}"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = f"{log_dir}/{name}.log"

        console_formatter = logging.Formatter("%(levelname)-10s[%(name)s] - %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)

        file_formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)-10s[%(name)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler = TimedRotatingFileHandler(filename=log_file, when="midnight", interval=1, backupCount=60)
        file_handler.suffix = "%Y%m%d"
        file_handler.namer = lambda name: name.replace(".log", "") + ".log"
        file_handler.extMatch = re.compile(r"\d{8}", re.ASCII)
        file_handler.setFormatter(file_formatter)

        self.log = logging.getLogger(name=f"{name.capitalize()}")
        self.log.setLevel(level=logging.DEBUG)
        self.log.addHandler(console_handler)
        self.log.addHandler(file_handler)


    def debug(self, msg_or_data):
        if ENV_MODE == "Development":
            self.log.debug(msg_or_data)


    def info(self, msg_or_data):
        self.log.info(msg_or_data)


    def warning(self, msg_or_data):
        self.log.warning(msg_or_data)


    def error(self, msg_or_data):
        self.log.error(msg_or_data)


    def critical(self, msg_or_data):
        self.log.critical(msg_or_data)
