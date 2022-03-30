from web_api.model.base_model import BaseModel, CreateUpdateMixin
from sqlalchemy import Column, String, Integer


class VideoModel(BaseModel, CreateUpdateMixin):
    """
    video
    """
    __tablename__ = "video"

    title = Column(String, nullable=False, comment='标题')
    link = Column(String, nullable=False, comment='链接')
    video_type = Column(Integer, nullable=False, comment="类型")
    video_status = Column(Integer, nullable=False, default=0, comment="状态")
