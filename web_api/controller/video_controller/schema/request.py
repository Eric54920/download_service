from pydantic import BaseModel, Field
from typing import Optional, List
from web_api.enum.video_enum import VideoEnum


class VideoRequestSchema(BaseModel):
    title: str = Field(..., title="标题")
    link: str = Field(..., title="链接")
    video_type: int = Field(..., title="视频类型")
    video_status: Optional[VideoEnum] = Field(0, title="视频状态")


class VideoUpdateRequestSchema(BaseModel):
    id: int = Field(..., title="id")
    title: Optional[str] = Field(None, title="标题")
    link: Optional[str] = Field(None, title="链接")
    video_type: Optional[int] = Field(None, title="视频类型")
    video_status: Optional[VideoEnum] = Field(0, title="视频状态")


class VideoDeleteRequestSchema(BaseModel):
    ids: List[int]
