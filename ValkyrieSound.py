class Song:
    def __init__(self, title, artist, album, duration):
        self.title = title  # Название песни
        self.artist = artist  # Исполнитель
        self.album = album  # Альбом
        self.duration = duration  # Длительность в секундах

    def __str__(self):
        return f"{self.title} - {self.artist} ({self.album}) [{self.duration}s]"
    
song1 = Song("Imagine", "John Lennon", "Imagine", 183)

print(song1)

class Playlist:
    def __init__(self, name):
        self.name = name  # Название плейлиста
        self.songs = []  # Список песен в плейлисте

    def add_song(self, song):
        self.songs.append(song)  # Добавление песни в плейлист

    def remove_song(self, song):
        self.songs.remove(song)  # Удаление песни из плейлиста

    def __str__(self):
        return f"Playlist: {self.name} ({len(self.songs)} songs)"

class Library:
    def __init__(self):
        self.songs = []  # Список всех песен в библиотеке
        self.playlists = []  # Список всех плейлистов

    def add_song(self, song):
        self.songs.append(song)  # Добавление песни в библиотеку

    def create_playlist(self, name):
        playlist = Playlist(name)
        self.playlists.append(playlist)  # Создание нового плейлиста
        return playlist

    def __str__(self):
        return f"Library: {len(self.songs)} songs, {len(self.playlists)} playlists"

class Player:
    def __init__(self):
        self.current_song = None  # Текущая воспроизводимая песня

    def play(self, song):
        self.current_song = song  # Воспроизведение выбранной песни
        print(f"Playing: {song}")

    def stop(self):
        print(f"Stopped: {self.current_song}")
        self.current_song = None  # Остановка воспроизведения
