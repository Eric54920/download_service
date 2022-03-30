from pydantic import BaseModel, Field
from typing import Any, List

from ..util.log_util import LogUtil

logger = LogUtil.get_logger()


class DeleteRequestSchema(BaseModel):
    id_list: List[int] = Field(..., title='id列表')


class ResponseSchema(BaseModel):
    success: bool = True
    message: str = ''
    data: Any = None
    error_code: int = 0


def json_result(success: bool, message: str = '', data: any = None, error_code: int = 0) -> ResponseSchema:
    response = ResponseSchema()
    response.success = success
    response.message = message if message else ''
    response.data = data
    response.error_code = error_code
    if not success:
        logger.info(message)
    return response
