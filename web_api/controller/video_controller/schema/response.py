from pydantic import BaseModel, Field
from typing import List
from ...base_schema import ResponseSchema


class VideoResponseModel(ResponseSchema):
    class Data(BaseModel):
        id: str = Field(..., title="ID")
        title: str = Field(..., title="标题")
        link: str = Field(..., title="链接")
        video_status: int = Field(..., title="状态")
        video_type: int = Field(..., title="分类")
        create_time: str = Field(..., title="创建时间")

    data: Data


class VideoListResponseModel(ResponseSchema):
    class Data(BaseModel):
        id: str = Field(..., title="ID")
        title: str = Field(..., title="标题")
        link: str = Field(..., title="链接")
        video_status: int = Field(..., title="状态")
        video_type: int = Field(..., title="分类")
        create_time: str = Field(..., title="创建时间")
        update_time: str = Field(..., title="更新时间")

    data: List[Data]


class VideoUpdateResponseModel(ResponseSchema):
    class Data(BaseModel):
        id: str = Field(..., title="ID")
        title: str = Field(..., title="标题")
        link: str = Field(..., title="链接")
        video_status: int = Field(..., title="状态")
        video_type: int = Field(..., title="分类")
        create_time: str = Field(..., title="创建时间")

    data: Data
