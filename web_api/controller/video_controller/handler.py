from fastapi import APIRouter, HTTPException, Depends

from web_api.service.video_service.video_service import VideoService
from .schema.request import VideoRequestSchema, VideoUpdateRequestSchema, VideoDeleteRequestSchema
from .schema.response import VideoResponseModel, VideoListResponseModel, VideoUpdateResponseModel
from ..base_schema import json_result, ResponseSchema
from ...util.log_util import LogUtil

logger = LogUtil.get_logger()

router = APIRouter()


@router.post("/video", response_model=VideoResponseModel, summary='新增视频')
def video(data: VideoRequestSchema):
    try:
        video = VideoService().create_video(data.dict(exclude_unset=True))
        return json_result(True, '新增视频成功', video)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, '新增视频失败')


@router.get("/video", response_model=VideoListResponseModel, summary="查询视频")
def video():
    try:
        videos = VideoService().query_videos()
        return json_result(True, "查询视频成功", videos)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, "查询视频失败")


@router.patch("/video", response_model=VideoUpdateResponseModel, summary="更新视频")
def video(data: VideoUpdateRequestSchema):
    try:
        videos = VideoService().update_videos(data.dict(exclude_unset=True))
        return json_result(True, "更新视频成功", videos)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, "更新视频失败")


@router.delete("/video", response_model=ResponseSchema, summary="删除视频")
def video(data: VideoDeleteRequestSchema):
    try:
        VideoService().delete_videos(data.dict())
        return json_result(True, '删除视频成功')
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, "删除视频失败")
