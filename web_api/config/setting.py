import os
import platform
from typing import Optional

from pydantic import BaseSettings
from .env_setting import ENV


class GlobalSetting(BaseSettings):
    TITLE: str = "Download Web Server"
    DESCRIPTION: str = "Download Web Server"

    VERSION: str = "1.0"

    SENTRY_DSN: Optional[str]

    LOG_LEVEL: str = os.environ.get('log_level', 'INFO')
    DEBUG: bool = eval(os.environ.get('debug', 'False'))

    SECRET_KEY: str = "change me"

    WEB_DIR_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DIR_SQL = os.path.join(WEB_DIR_HOME, 'sql')
    DIR_LOG = os.path.join(os.path.dirname(WEB_DIR_HOME), 'logs')
    if platform.system() == "Darwin":
        VIDEO_FILE_PATH = os.path.join(os.path.dirname(WEB_DIR_HOME), 'data/videos')
    else:
        VIDEO_FILE_PATH = "/var/lib/docker/volumes/opt_nextcloud/_data/data/realmaguodong/files/Movie/"


class SettingDev(GlobalSetting):
    pass


class SettingTest(GlobalSetting):
    pass


class SettingProd(GlobalSetting):
    pass


if ENV == 'test':
    setting = SettingTest()
elif ENV == 'prod':
    setting = SettingProd()
else:
    setting = SettingDev()
