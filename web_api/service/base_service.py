from web_api.util.db import db_session


class BaseService(object):

    session = db_session
