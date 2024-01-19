import os
from googleapiclient.discovery import build
from datetime import timedelta
import isodate

API_KEY = os.getenv('YT_API_KEY')


class PlayList:
    """инициализируется _id_ плейлиста и имеет следующие публичные атрибуты:
    - название плейлиста
    - ссылку на плейлист"""

    def __init__(self, playlist_id: str) -> None:
        self.playlist_id = playlist_id
        self.playlists = PlayList.get_service().playlists().list(id=playlist_id,
                                                                 part='contentDetails, snippet',
                                                                 maxResults=50,
                                                                 ).execute()
        # название плейлиста
        self.title: str = (self.playlists['items'][0]['snippet']['title'])
        # ссылка на плейлист
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        # продолжительность плейлиста
        self.__duration_playlist: timedelta = timedelta(hours=0, minutes=0, seconds=0)
        self.playlist_videos = PlayList.get_service().playlistItems().list(playlistId=playlist_id,
                                                                           part='contentDetails',
                                                                           maxResults=50,
                                                                           ).execute()
        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        # print(video_ids)
        self.video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                                   id=','.join(video_ids)
                                                                   ).execute()

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        return youtube

    @property
    def total_duration(self):
        """
        Выводит длительности видеороликов из плейлиста
        """
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            self.__duration_playlist += duration
        return self.__duration_playlist

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста
        (по количеству лайков)"""
        max_like_count = 0
        url_best_video = ""
        for video in self.video_response['items']:
            # количество лайков
            like_count: int = int(video['statistics']['likeCount'])
            if max_like_count < like_count:
                max_like_count = like_count
                # ссылка на видео
                url_best_video = f"https://youtu.be/{video['id']}"
        return url_best_video
