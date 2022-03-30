from sqlalchemy import text, distinct
from web_api.dao.base_dao import BaseDao, Session
from web_api.model.video_model import VideoModel

class VideoDao(BaseDao):
    
    def query_videos(self, session: Session):
        return session.query(self.model).filter(
            self.model.is_delete == 0
        )


video_dao = VideoDao(VideoModel)