from fastapi import HTTPException

from web_api.dao.video_dao import video_dao
from ..base_service import BaseService


class VideoService(BaseService):

    @classmethod
    def create_video(cls, data):
        with cls.session() as sess:
            if video_dao.check_unique(sess, "title", data['title']):
                raise HTTPException(400, '标题已存在')

            video = video_dao.create(session=sess, obj_in=data)
        return video.to_dict()

    @classmethod
    def query_videos(cls):
        with cls.session() as sess:
            videos = video_dao.query_videos(session=sess)
        return [i.to_dict() for i in videos]

    @classmethod
    def update_videos(cls, data):
        with cls.session() as sess:
            video_obj = video_dao.get(sess, data['id'])

            if not video_obj:
                raise HTTPException(404, "不存在该视频")

            if data.get('title'):
                if video_dao.check_unique(sess, "title", data['title']):
                    raise HTTPException(400, "该标题已存在")

            video = video_dao.update(sess, db_obj=video_obj, obj_in=data)
            return video.to_dict()

    @classmethod
    def delete_videos(cls, data):
        with cls.session() as sess:
            video_dao.logically_delete(sess, data['ids'])
