
from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ValidationError
from starlette.middleware.cors import CORSMiddleware

from .config.setting import setting
from .controller.video_controller.handler import router as video_router
from .util.db import init_db, update_db
from .util.log_util import LogUtil

logger = LogUtil.get_logger()


def setup_routers(app: FastAPI):
    api_router = APIRouter()
    api_router.include_router(
        video_router, prefix="/api/video", tags=["video"])

    app.include_router(api_router)


def setup_logging(app: FastAPI):
    pass


def setup_middleware(app: FastAPI):

    @app.exception_handler(HTTPException)
    def http_exception_handler(request: Request, exc: HTTPException):
        msg = str(exc.detail)
        logger.info(msg)
        return JSONResponse(
            status_code=exc.status_code,
            content={'success': False, 'message': msg,
                     'data': None, 'error_code': exc.status_code}
        )

    @app.exception_handler(RequestValidationError)
    def request_validation_error_handler(request: Request, exc: RequestValidationError):
        msg = str(['.'.join([str(i) for i in error.get('loc')]) +
                   ':' + error.get('msg') for error in exc.errors()])
        logger.info(msg)
        return JSONResponse(
            status_code=422,
            content={'success': False, 'message': msg,
                     'data': None, 'error_code': 422}
        )

    @app.exception_handler(ValidationError)
    def response_validation_error_handler(request: Request, exc: ValidationError):
        msg = str(exc.raw_errors)
        logger.info(msg)
        return JSONResponse(
            status_code=500,
            content={'success': False, 'message': msg,
                     'data': None, 'error_code': 500}
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def setup_sentry(app):
    # import sentry_sdk
    #
    # sentry_sdk.init(
    #     "sentry_sdk",
    # )

    pass


def create_app():
    app = FastAPI(
        debug=setting.DEBUG,
        title=setting.TITLE,
        description=setting.DESCRIPTION,
    )

    # 初始化路由
    setup_routers(app)
    # 初始化全局 middleware
    setup_middleware(app)
    # 初始化全局 logging
    setup_logging(app)
    # 初始化 sentry
    if setting.SENTRY_DSN:
        setup_sentry(app)

    return app
