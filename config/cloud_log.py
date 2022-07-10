import datetime
import socket
import time
import logging
import os
import sys
from loguru import logger

# logger.opt(depth-depth, exception-record.exc_info).log(level, record.getMessage())

# class supports logging of other packages with loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


LEVELS = ['TRACE', "DEBUG", "INFO", "SUCCESS", "WARNING", 'ERROR', 'CRITICAL', None]


# this function is called in main.py to setup logging for our script
def setup_logging(log_config: dict):
    logging.root.handlers = [InterceptHandler()]
    log_level = os.environ.get("LOG_LEVEL", "DEBUG")
    logging.root.setLevel(log_level)

    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    val = datetime.datetime.now().astimezone().tzinfo

    if val == datetime.timezone(datetime.timedelta(0), name='UTC'):
        os.environ['TZ'] = 'America/New_York'
        time.tzset()
        print(f"Current Time - adjusted: {datetime.datetime.now()}")
    else:
        print(f"Timezone: {val}")
        print(f"Current Time - unadjusted: {datetime.datetime.now()}")

    application = os.environ.get("APPLICATION_NAME", "unnamed")
    container = socket.gethostname()

    logger.remove()
    for k, v in log_config.items():
        if v is None or str(v).upper() == 'NONE':
            logger.debug(f"Skipping configuration {k} as value is None")

        elif not isinstance(v, str) or str(v).upper() not in LEVELS:
            logger.debug(f"Logging type {k} has improper value {v}")

        elif k == 'LOCAL_CONSOLE' and isinstance(v, str):
            logger.add(
                sys.stdout,
                format='<g>{time:YYY-MM-DD HH:mm:ss:SSS ZZ}</>|<lvl>{level}</>|{process}|{thread}|{name}|{function}|{line}|<lvl>{message}</>',
                level=v.upper(),
                enqueue=True
            )
            logger.info("Console logging added at level {}", v)

        elif k == 'HUMIO' and isinstance(v, str):
            logger.add(
                sys.stdout,
                format ='"<g›{time:YYY-MM-DD HH:mm:ss:SSS ZZ}</›", "‹lvl›{level}‹/>", "<lvl>{message}</>"',
                level=v.upper(),
                enqueue=True,
                serialize=True
                )
            logger.info("HUMIO logging via console added at level {}", v)

        # elif k == NAS_FILE ?
        else:
            print(f"Unknown type {k} with value {v}")

    logger.debug("DEBUG")
    logger.info("INFO")
    logger.success("SUCCESS")
    logger.warning("WARNING")
    logger.error("ERROR")
