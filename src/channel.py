import json
import os
from googleapiclient.discovery import build


API_KEY = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """
        1. Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        2. Модифицируйте конструктор `Channel`, чтобы после инициализации экземпляр имел следующие атрибуты,
        заполненные реальными данными канала:
        """
        self.__channel_id = channel_id
        channel = Channel.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        # Название канала
        self.title = channel['items'][0]['snippet']['title']
        # Описание кана
        self.info = channel["items"][0]["snippet"]["description"]
        # ссылка на канал
        self.url = channel["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        # - количество подписчиков
        self.subscriber_count = channel["items"][0]["statistics"]["subscriberCount"]
        # - количество видео
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        # - общее количество просмотров
        self.view_count = channel["items"][0]["statistics"]["viewCount"]

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        return youtube

    # @property
    # def channel_id(self):
    #     return self.__channel_id

    # getter channel_id "закомментировала", т.к. при запуске moscowpython.channel_id = 'Новое название'
    # выдает ошибку: AttributeError: property 'channel_id' of 'Channel' object has no setter
    # и "падает" код, не доходит до print(Channel.get_service()) и moscowpython.to_json('moscowpython.json')

    def __str__(self):
        """Возвращает название и ссылку на канал по шаблону `<название_канала> (<ссылка_на_канал>)`"""
        return f"'{self.title} ({self.url})'"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __rsub__(self, other):
        return int(other.subscriber_count) - int(self.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    def print_info(self) -> None:
        """
        Выводит в консоль информацию о канале.
        """
        instance_data = Channel.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(instance_data, indent=2, ensure_ascii=False))

    def to_json(self, file_json):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`
        создает файл 'moscowpython.json' с данными по каналу"""
        instance_data = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.info,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(file_json, "w", encoding="utf-8") as file:
            json.dump(instance_data, file, indent=2, ensure_ascii=False)
