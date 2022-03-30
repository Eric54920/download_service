from os import path, environ
from .env_setting import ENV


class BaseDbSetting(object):
    # sqlite配置
    SQLITE_DATA_FILE_PATH = path.dirname(
        path.dirname(path.dirname(path.abspath(__file__)))) + '/data/sqlite/videos.db'.replace('/', path.sep)
    DATABASE_URL: str = 'sqlite:///' + SQLITE_DATA_FILE_PATH


class DbSettingDev(BaseDbSetting):
    pass


class DbSettingTest(BaseDbSetting):
    pass


class DbSettingProd(BaseDbSetting):
    pass


if ENV == 'test':
    db_setting = DbSettingTest()
elif ENV == 'prod':
    db_setting = DbSettingProd()
else:
    db_setting = DbSettingDev()
