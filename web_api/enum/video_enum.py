from enum import Enum


class VideoEnum(int, Enum):
    UNDOWNLOAD = 0
    DOWNLOADING = 1
    DONE = 2
    ERROR = 3