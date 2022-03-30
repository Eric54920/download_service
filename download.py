import sqlite3
import time
import os
from threading import Thread, RLock
import logging.config
import asyncio
import aiohttp
from queue import Queue
from web_api.config.db_setting import db_setting
from web_api.config.setting import setting

logging.basicConfig(
    filename='./logs/download.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(threadName)s] [%(name)s] [%(levelname)s] %(filename)s[line:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class DownloadService():
    status_enum = {
        "undownload": 0,
        "downloading": 1,
        "done": 2,
        "error": 3
    }

    def __init__(self):
        self.table_name = "video"
        self.__daemon = True
        self.stopped = False
        self.__connection = None
        self.__connected = False
        self.lock = RLock()
        self.status_queue = Queue(-1)

    def execute(self, *args):
      
        try:
            with self.lock:
                return self.__connection.execute(*args)
        except Exception as e:
            logging.exception(e)

    def commit(self):
        
        try:
            with self.lock:
                self.__connection.commit()
        except Exception as e:
            logging.exception(e)

    def rollback(self):

        try:
            with self.lock:
                self.__connection.rollback()
        except Exception as e:
            logging.exception(e)

    def connect_db(self):
        logging.info("connect starting...")
        while not self.stopped:
            if self.__connection is None:
                try:
                    db_path = db_setting.SQLITE_DATA_FILE_PATH
                    self.__connection = sqlite3.connect(db_path, check_same_thread=False)
                    logging.info("connect success")
                    self.__connected = True
                except Exception as e:
                    self.__connected = False
                    logging.error(e)

            time.sleep(1)

    def read_data(self):
        try:
            data = self.execute(f"SELECT * FROM {self.table_name} WHERE video_status = 0 and is_delete=0;")
            return data
        except Exception as e:
            self.rollback()
            logging.exception(e)

    def change_status(self):
        logging.info("change status starting")
        
        while not self.stopped:
            if self.status_queue.qsize() > 0:
                try:
                    item = self.status_queue.get()
                    logging.info(f"{item[0][1]} change status => {item[1]}")
                    self.execute(f"update {self.table_name} set video_status={item[1]} where id={item[0][0]}")
                    self.commit()
                except Exception as e:
                    logging.error(e)

            time.sleep(0.1)

    async def download(self, item):

        self.status_queue.put([item, self.status_enum['downloading']])

        try:
            logging.info(f"Start Download {item[1]}")

            async with aiohttp.ClientSession() as session:
                async with await session.get(item[2], verify_ssl=False) as response:
                    ext = item[2].split(".")[-1]
                    res = await response.read()
                    file_path = os.path.join(setting.VIDEO_FILE_PATH, f"{item[1]}.{ext}")
                    with open(file_path, 'wb') as f:
                        f.write(res)

            logging.info(f"Download [{item[1]}] Done")
        except Exception as e:
            logging.exception(e)
            self.status_queue.put([item, self.status_enum['error']])
        else:
            self.status_queue.put([item, self.status_enum['done']])

    def run(self):
        logging.info("starting...")
        # 连接sql
        connect_thread = Thread(target=self.connect_db, daemon=self.__daemon)
        connect_thread.start()

        status_thread = Thread(target=self.change_status, daemon=self.__daemon)
        status_thread.start()

        logging.info("check starting...")
        
        tasks = []
        loop = asyncio.get_event_loop()
        while not self.stopped:
            if self.__connection and self.__connected:
                try:
                    data = self.read_data().fetchall()
                    if data:
                        for item in data:
                            c = self.download(item)
                            task = loop.create_task(c)
                            tasks.append(task)

                        loop.run_until_complete(asyncio.wait(tasks))
                    
                except Exception as e:
                    logging.error(e)
                
                time.sleep(60)

# if __name__ == "__main__":
#     download_service = DownloadService()
#     download_service.run()


