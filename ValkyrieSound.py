from abc import ABC, abstractmethod
from collections import deque

# Создайте иерархию пользовательских исключений (например, BaseException -> CustomError -> SpecificError). Обработайте каждое исключение по-разному в зависимости от его типа
class BaseError(Exception):
    """Базовый класс для других исключений."""
    pass

class CustomError(BaseError):
    """Класс для ошибок, связанных с обработкой музыки."""
    pass

class SpecificError(CustomError):
    """Класс для специфичных ошибок, связанных с плейлистами."""
    pass
# Базовый класс: задание 3
class MusicObject(ABC):
    @abstractmethod
    def __str__(self):
        pass

# Производные классы:
class Song(MusicObject):
    def __init__(self, title, artist, album, duration):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
# Переопределяется 
    def __str__(self):
        return f"{self.title} by {self.artist}"
    
# Производные классы:
# защищённые атрибуты 
class SongWithOperator(Song):
    def __init__(self, title, artist, album, duration):
        super().__init__(title, artist, album, duration)  # Вызов конструктора базового класса
        self._duration = duration  # Защищенный атрибут

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
# Задание 6:   
    def __repr__(self):
        return f"SongWithOperator(title={self.title!r}, artist={self.artist!r}, album={self.album!r}, duration={self.duration})"

class Playlist(MusicObject):
    total_playlists = 0

    def __init__(self, name):
        self.name = name
        self.songs = deque()
        Playlist.total_playlists += 1

    def add_song(self, song):
        if not isinstance(song, SongWithOperator):
            raise SpecificError("Only SongWithOperator instances can be added.") # использование райс для генерации собственных исключений 
        self.songs.append(song)

    def remove_song(self):
        if self.songs:
            return self.songs.popleft()
        raise SpecificError("No songs to remove.")

    def __str__(self):
        song_titles = ', '.join(str(song) for song in self.songs)
        return f"Playlist: {self.name} with songs: {song_titles}"

    @classmethod
    def get_total_playlists(cls):
        return cls.total_playlists

    def find_song_with_max_duration(self):
        if not self.songs:
            raise SpecificError("Cannot find songs in an empty playlist.")
        max_song = max(self.songs, key=lambda song: song.duration)
        return max_song

class MusicLibrary:
    def __init__(self):
        self.songs = []  # Одномерный список
        self.playlists = []  # Двумерный список плейлистов

    def add_song(self, song):
        self.songs.append(song)

    def add_playlist(self, playlist):
        self.playlists.append(playlist)

    def find_max_duration_song(self):
        if not self.songs:
            raise SpecificError("No songs available to find.")
        return max(self.songs, key=lambda song: song.duration)

class User:
    def __init__(self, username):
        self.username = username
        self.library = []
        self.playlists = []

    def add_song_to_library(self, song):
        self.library.append(song)

    def create_playlist(self, name):
        playlist = Playlist(name)
        self.playlists.append(playlist)
        return playlist

    def play_song(self, song):
        print(f"Playing: {song}")

    def stop_song(self):
        print("Song stopped.")

    def __str__(self):
        return f"User: {self.username}, Library: {[str(song) for song in self.library]}"

def main():
    user = User("JohnDoe")
    music_library = MusicLibrary()  # Создание библиотеки музыки

    # Создание песен
    song1 = SongWithOperator("Song 1", "Artist 1", "Album 1", 210)
    song2 = SongWithOperator("Song 2", "Artist 2", "Album 2", 180)
    
    # Добавление песен в библиотеку
    user.add_song_to_library(song1)
    user.add_song_to_library(song2)
    music_library.add_song(song1)
    music_library.add_song(song2)

    # Задание 1 обработка исключений 
    playlist = user.create_playlist("My Playlist")
    try:
        playlist.add_song(song1)
        playlist.add_song(song2)
    except SpecificError as e:
        print(f"SpecificError occurred: {e}")  # Обработка SpecificError
    except CustomError as e:
        print(f"CustomError occurred: {e}")    # Обработка CustomError
    except BaseError as e:
        print(f"BaseError occurred: {e}")      # Обработка BaseError
    finally:
        print(f"Total playlists created: {Playlist.get_total_playlists()}")  # Обязательный код

    try:
        # Воспроизведение песни
        user.play_song(song1)
        user.stop_song()

        # Поиск песни с максимальной длительностью
        longest_song = playlist.find_song_with_max_duration()
        print(f"Longest song in the playlist: {longest_song}")
        
        # Удаление песни
        removed_song = playlist.remove_song()
        print(f"Removed song: {removed_song}")

    except SpecificError as e:
        print(f"Error: {e}")
    finally:
        print("Playlist operations complete.")

    # Вывод информации о библиотеке
    print(user)

    # Демонстрация перегрузки операторов
    song3 = song1 + song2
    print(f"Combined Song: {song3}")

# Запуск основной функции, если файл запущен как основная программа
if __name__ == "__main__":
    main()