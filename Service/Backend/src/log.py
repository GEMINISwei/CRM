# =====================================================================================================================
#                   Import
# =====================================================================================================================
from os import environ, path, getcwd, makedirs
from re import compile, ASCII
from logging import Formatter, StreamHandler, getLogger, DEBUG
from logging.handlers import TimedRotatingFileHandler


# =====================================================================================================================
#                   Class
# =====================================================================================================================
class LogFile:
    def __init__(self, name: str, enabled: bool=True):
        current_work_dir = getcwd()
        log_dir = f"{current_work_dir}/../logs/{name}"
        if not path.exists(log_dir):
            makedirs(log_dir)

        log_file = f"{log_dir}/{name}.log"

        console_formatter = Formatter("%(levelname)-10s[%(name)s] - %(message)s")
        console_handler = StreamHandler()
        console_handler.setFormatter(console_formatter)

        file_formatter = Formatter(
            fmt="%(asctime)s %(levelname)-10s[%(name)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler = TimedRotatingFileHandler(filename=log_file, when="midnight", interval=1, backupCount=60)
        file_handler.suffix = "%Y%m%d"
        file_handler.namer = lambda name: name.replace(".log", "") + ".log"
        file_handler.extMatch = compile(r"\d{8}", ASCII)
        file_handler.setFormatter(file_formatter)

        self.log = getLogger(name=f"{name.capitalize()}")
        self.log.setLevel(level=DEBUG)
        self.log.addHandler(console_handler)
        self.log.addHandler(file_handler)

        self.enabled = enabled

    def debug(self, msg_or_data):
        if self.enabled:
            if ENV_MODE == "Development":
                self.log.debug(msg_or_data)

    def info(self, msg_or_data):
        if self.enabled:
            self.log.info(msg_or_data)

    def warning(self, msg_or_data):
        if self.enabled:
            self.log.warning(msg_or_data)

    def error(self, msg_or_data):
        if self.enabled:
            self.log.error(msg_or_data)

    def critical(self, msg_or_data):
        if self.enabled:
            self.log.critical(msg_or_data)


# =====================================================================================================================
#                   Variable
# =====================================================================================================================
ENV_MODE = environ["MODE"]
