import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from web_api.config.db_setting import ENV
from web_api.config.setting import setting


class LogUtil:
    LOG_FORMAT = '%(asctime)s %(levelname)s [%(thread)d-%(threadName)s] %(module)s.%(funcName)s:%(lineno)d %(message)s'

    @staticmethod
    def get_logger(logger_name='web_server', log_level=None):
        if log_level is None:
            if ENV == 'prod':
                log_level = logging.INFO
            else:
                log_level = logging.INFO

        logger = logging.getLogger(logger_name)
        if not logger.hasHandlers():
            fmt = logging.Formatter(
                fmt=LogUtil.LOG_FORMAT,
                datefmt="[%Y/%m/%d-%H:%M:%S]"
            )
            stream_handler = logging.StreamHandler(stream=sys.stdout)
            stream_handler.setFormatter(fmt)
            logger.addHandler(stream_handler)

            log_file = os.path.join(setting.DIR_LOG, f'{logger_name}.log')
            file_handler = TimedRotatingFileHandler(log_file, 'midnight', 1, 15)
            file_handler.setFormatter(fmt)
            logger.addHandler(file_handler)

            logger.setLevel(log_level)

        return logger