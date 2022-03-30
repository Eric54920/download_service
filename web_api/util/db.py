from os import path, makedirs, listdir
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from .log_util import LogUtil
from ..config.db_setting import db_setting
from ..config.setting import setting

engine = create_engine(db_setting.DATABASE_URL, pool_pre_ping=True)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

logger = LogUtil.get_logger('web_server')


def init_db():
    dir_db_path = path.dirname(db_setting.SQLITE_DATA_FILE_PATH)
    if not path.exists(dir_db_path):
        makedirs(dir_db_path)

    dir_video_path = setting.VIDEO_FILE_PATH
    if not path.exists(dir_video_path):
        makedirs(dir_video_path)

    Base.metadata.reflect(engine)
    tables = Base.metadata.tables
    try:
        if 'db_history' not in tables:
            print(1)
            sql_file_path = path.join(setting.DIR_SQL, '1.0.init.sql')
            with open(sql_file_path, 'r') as f:
                init_sql = f.read()

            sql_list = init_sql.split(';')
            sql_list = [i.strip() for i in sql_list]

            with db_session() as session:
                for sql in sql_list:
                    session.execute(sql)
                session.commit()

            logger.info('init db success.')
            return True

        else:
            return True
    except Exception as e:
        logger.exception(e)
        return False


def update_db():
    sql_files = listdir(setting.DIR_SQL)
    sql_files.sort()

    try:
        with db_session() as session:
            db_history = session.execute(
                "SELECT sql_name FROM db_history;"
            )
            sql_name_list = [i[0] for i in list(db_history)]
            sql_name_list.sort()

            for sql_file in sql_files:
                if sql_file not in sql_name_list:
                    sql_file_path = path.join(setting.DIR_SQL, sql_file)
                    with open(sql_file_path, 'r') as f:
                        sql_content = f.read()

                    sql_list = sql_content.split(';')
                    sql_list = [i.strip() for i in sql_list]
                    for sql in sql_list:
                        session.execute(sql)

                    session.execute(f"""INSERT INTO db_history (sql_name, content) VALUES ("{sql_file}", "{sql_content}");""")
                    session.commit()
                    logger.info(f'execute sql：{sql_file} success.')

            return True
    except Exception as e:
        logger.exception(e)
        return False

