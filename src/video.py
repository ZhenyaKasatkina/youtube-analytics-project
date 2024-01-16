import os
from googleapiclient.discovery import build


API_KEY = os.getenv('YT_API_KEY')


class Video:
    """Класс для ютуб-видео"""

    def __init__(self, video_id: str) -> None:
        """
        1. Экземпляр инициализируется id видео из ютуб
        Дальше все данные будут подтягиваться по API.
        """
        # id видео
        self.video_id = video_id
        video_response = Video.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                           id=video_id
                                                           ).execute()
        # print(f"видео: {video_response}")

        # Название видео
        self.video_title: str = video_response['items'][0]['snippet']['title']
        # ссылка на видео
        self.url = f"https://www.youtube.com/watch?v/{self.video_id}"
        # количество просмотров
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        # # количество лайков
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        return youtube

    def __str__(self):
        return self.video_title


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str) -> None:
        """
        1. Экземпляр инициализируется по id видео и id плейлиста из ютуб
        Дальше все данные будут подтягиваться по API.
        2. Реализуйте инициализацию реальными данными следующих атрибутов экземпляра класса `PLVideo`:
        - id видео
        - название видео
        - ссылка на видео
        - количество просмотров
        - количество лайков
        - id плейлиста
        """
        super().__init__(video_id)
        self.playlist_id = playlist_id

        # playlist_videos = PLVideo.get_service().playlistItems().list(playlistId=playlist_id,
        #                                                              part='contentDetails',
        #                                                              maxResults=50,
        #                                                              ).execute()
        # print(f"Плейлист: {playlist_videos}")
