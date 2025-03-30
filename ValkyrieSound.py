import logging
from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime

# Настройка логирования
logging.basicConfig(filename='music_library.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Создайте иерархию пользовательских исключений
class BaseError(Exception):
    """Базовый класс для других исключений."""
    def __init__(self, message, context=None):
        super().__init__(message)
        self.context = context

    def __str__(self):
        return f"{self.args[0]} (Context: {self.context})"

class CustomError(BaseError):
    """Класс для ошибок, связанных с обработкой музыки."""
    pass

class SpecificError(CustomError):
    """Класс для специфичных ошибок, связанных с плейлистами."""
    pass

# Базовый класс
class MusicObject(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def play(self):
        pass  # Полиморфный метод, который будет переопределен в производных классах

# Производные классы
class Song(MusicObject):
    def __init__(self, title, artist, album, duration):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        logging.info(f"Created Song: {self}")  # Логирование создания песни

    def __str__(self):
        return f"{self.title} by {self.artist}"

    def play(self):
        logging.info(f"Playing song: {self}")  # Логирование воспроизведения песни
        return f"Playing: {self.title}"

    def __add__(self, other):
        if isinstance(other, Song):
            return Song(
                title=f"{self.title} & {other.title}",
                artist=self.artist,
                album=self.album,
                duration=self.duration + other.duration
            )
        return NotImplemented

class SongWithOperator(Song):
    def __init__(self, title, artist, album, duration):
        super().__init__(title, artist, album, duration)
        self._duration = duration

    def __add__(self, other):
        if isinstance(other, SongWithOperator):
            return SongWithOperator(
                title=f"{self.title} & {other.title}",
                artist=self.artist,
                album=self.album,
                duration=self.duration + other.duration
            )
        return NotImplemented

    def __lt__(self, other):
        return self.duration < other.duration

    def __eq__(self, other):
        return self.duration == other.duration

    def __repr__(self):
        return f"SongWithOperator(title={self.title!r}, artist={self.artist!r}, album={self.album!r}, duration={self.duration})"

    def play(self):
        logging.info(f"Playing song with operator: {self}")  # Логирование воспроизведения песни с оператором
        return f"Playing: {self.title}"

class Playlist(MusicObject):
    total_playlists = 0

    def __init__(self, name):
        self.name = name
        self.songs = deque()
        Playlist.total_playlists += 1
        logging.info(f"Created Playlist: {self.name}")  # Логирование создания плейлиста

    def add_song(self, song):
        if not isinstance(song, SongWithOperator):
            raise SpecificError("Only SongWithOperator instances can be added.", context={"playlist": self.name, "song": song})
        self.songs.append(song)
        logging.info(f"Added song to playlist '{self.name}': {song}")  # Логирование добавления песни в плейлист

    def remove_song(self):
        if self.songs:
            removed_song = self.songs.popleft()
            logging.info(f"Removed song from playlist '{self.name}': {removed_song}")  # Логирование удаления песни из плейлиста
            return removed_song
        raise SpecificError("No songs to remove.", context={"playlist": self.name})

    def play(self):
        if not self.songs:
            raise SpecificError("No songs in the playlist to play.", context={"playlist": self.name})
        # Воспроизведение всех песен в плейлисте
        logging.info(f"Playing playlist: {self.name}")  # Логирование воспроизведения плейлиста
        return [song.play() for song in self.songs]

    def __str__(self):
        song_titles = ', '.join(str(song) for song in self.songs)
        return f"Playlist: {self.name} with songs: {song_titles}"

    @classmethod
    def get_total_playlists(cls):
        return cls.total_playlists

    def find_song_with_max_duration(self):
        if not self.songs:
            raise SpecificError("Cannot find songs in an empty playlist.", context={"playlist": self.name})
        max_song = max(self.songs, key=lambda song: song.duration)
        logging.info(f"Found longest song in playlist '{self.name}': {max_song}")  # Логирование поиска самой длинной песни
        return max_song

class MusicLibrary:
    def __init__(self):
        self.songs = []
        self.playlists = []
        logging.info("Initialized Music Library")  # Логирование инициализации библиотеки музыки

    def add_song(self, song):
        self.songs.append(song)
        logging.info(f"Added song to library: {song}")  # Логирование добавления песни в библиотеку

    def add_playlist(self, playlist):
        self.playlists.append(playlist)
        logging.info(f"Added playlist to library: {playlist.name}")  # Логирование добавления плейлиста в библиотеку

    def find_max_duration_song(self):
        if not self.songs:
            raise SpecificError("No songs available to find.")
        max_song = max(self.songs, key=lambda song: song.duration)
        logging.info(f"Found longest song in library: {max_song}")  # Логирование поиска самой длинной песни в библиотеке
        return max_song

class User:
    def __init__(self, username):
        self.username = username
        self.library = []
        self.playlists = []
        logging.info(f"Created User: {self.username}")  # Логирование создания пользователя

    def add_song_to_library(self, song):
        self.library.append(song)
        logging.info(f"User '{self.username}' added song to library: {song}")  # Логирование добавления песни в библиотеку пользователя

    def create_playlist(self, name):
        playlist = Playlist(name)
        self.playlists.append(playlist)
        return playlist

    def play_song(self, song):
        return song.play()  # Вызов полиморфного метода play

    def stop_song(self):
        logging.info("Song stopped.")  # Логирование остановки песни
        return "Song stopped."

    def __str__(self):
        return f"User: {self.username}, Library: {[str(song) for song in self.library]}"

def main():
    user = User("JohnDoe")
    music_library = MusicLibrary()

    # Создание песен
    song1 = Song("Song 1", "Artist 1", "Album 1", 210)
    song2 = SongWithOperator("Song 2", "Artist 2", "Album 2", 180)

    # Добавление песен в библиотеку
    user.add_song_to_library(song1)
    user.add_song_to_library(song2)
    music_library.add_song(song1)
    music_library.add_song(song2)

    # Обработка исключений при добавлении песен в плейлист
    playlist = user.create_playlist("My Playlist")
    try:
        playlist.add_song(song2)  # Добавляем песню в плейлист
    except SpecificError as e:
        print(f"SpecificError occurred: {e}")
    except CustomError as e:
        print(f"CustomError occurred: {e}")
    except BaseError as e:
        print(f"BaseError occurred: {e}")
    finally:
        print(f"Total playlists created: {Playlist.get_total_playlists()}")

    try:
        # Воспроизведение песни
        print(user.play_song(song1))  # Вызов полиморфного метода play
        user.stop_song()

        # Воспроизведение плейлиста
        print(playlist.play())

        # Поиск песни с максимальной длительностью
        longest_song = playlist.find_song_with_max_duration()
        print(f"Longest song in the playlist: {longest_song}")

        # Удаление песни
        removed_song = playlist.remove_song()
        print(f"Removed song: {removed_song}")

        # Пример сложения песен
        combined_song = song1 + song2  # Используем сложение для Song и SongWithOperator
        print(f"Combined Song: {combined_song}")

        # Пример использования лямбда-выражений для сортировки
        sorted_songs = sorted(music_library.songs, key=lambda song: song.duration)  # Сортировка песен по длительности
        print("Songs sorted by duration:")
        for song in sorted_songs:
            print(song)

    except SpecificError as e:
        print(f"Error: {e}")
    finally:
        print("Playlist operations complete.")

    # Вывод информации о библиотеке
    print(user)

# Запуск основной функции, если файл запущен как основная программа
if __name__ == "__main__":
    main()