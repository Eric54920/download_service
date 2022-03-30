from os import mkdir, path
from web_api.config.setting import setting
if not path.exists(setting.DIR_LOG):
    mkdir("logs")
from web_api.app import create_app
from web_api.app import init_db, update_db
from download import DownloadService
from multiprocessing import Process
print("aaa")


def service():
    download_service = DownloadService()
    download_service.run()


def web_api():
    import uvicorn
    uvicorn.run(app='start:create_app', host='0.0.0.0',
                port=8009, reload=False)


def run():
    if not init_db():
        return

    if not update_db():
        return

    p_list = []
    p1 = Process(target=service, name='run_main_gateway_service')
    p_list.append(p1)
    p2 = Process(target=web_api, name='run_web_api')
    p_list.append(p2)

    for p in p_list:
        p.daemon = True
        p.start()
    for p in p_list:
        p.join()


if __name__ == "__main__":
    run()
