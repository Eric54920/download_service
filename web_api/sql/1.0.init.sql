-- video
CREATE TABLE IF NOT EXISTS video(
    id INTEGER PRIMARY KEY NOT NULL,
    title VARCHAR UNIQUE NOT NULL,
    link VARCHAR NOT NULL,
    video_type INTEGER NOT NULL,
    video_status INTEGER NOT NULL DEFAULT 0,
    is_delete INTEGER NOT NULL DEFAULT 0,
    create_time TimeStamp NOT NULL DEFAULT (datetime('now','localtime')),
    update_time TimeStamp NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS db_history(
    id INTEGER PRIMARY KEY NOT NULL,
    sql_name VARCHAR NOT NULL DEFAULT '',
    content VARCHAR NOT NULL DEFAULT '',
    create_time TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO db_history (sql_name, content) VALUES ('1.0.init.sql', '');