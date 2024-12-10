import sys
from pprint import pprint
import inspect
import hashlib
import time


def introspection_info(obj):
    print(type(obj))
    pprint(dir(obj))
    print(callable(obj))
    module = inspect.getmodule(introspection_info)
    print(module)
    print(sys.getsizeof(obj))


class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = self.hash_password(password)
        self.age = age

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def __str__(self):
        return self.nickname


class Video:
    def __init__(self, title, duration, time_now=0, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = time_now
        self.adult_mode = adult_mode

    def __str__(self):
        return self.title


class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, nickname, password):
        for user in self.users:
            if user.nickname == nickname and user.password == user.hash_password(password):
                self.current_user = user
                print(f"Пользователь {nickname} успешно вошел в аккаунт.")
                return
            else:
                print("Неверный логин или пароль.")

    def register(self, nickname, password, age):
        if any(user.nickname == nickname
               for user in self.users):
            print(f"Пользователь {nickname} уже существует")
        else:
            new_user = User(nickname, password, age)
            self.users.append(new_user)
            self.current_user = new_user
            print(f"Пользователь {nickname} зарегистрирован и вошел в аккаунт.")

    def log_out(self):
        self.current_user = None
        print("Вы вышли из аккаунта.")

    def add(self, *videos):
        for video in videos:
            if not any(v.title == video.title for v in self.videos):
                self.videos.append(video)
                print(f"Видео '{video.title}' добавлено.")
            else:
                print(f"Видео '{video.title}' уже существует.")

    def get_videos(self, keyword):
        return [video.title for video in self.videos if keyword.lower() in video.title.lower()]

    def watch_video(self, title):
        if self.current_user is None:
            print("Войдите в аккаунт, чтобы смотреть видео.")
            return

        video = next((v for v in self.videos if v.title == title), None)
        if video is None:
            print("Видео не найдено.")
            return

        if video.adult_mode and self.current_user.age < 18:
            print("Вам нет 18 лет, пожалуйста покиньте страницу.")
            return

        print(f"Начинаем просмотр видео '{video.title}'.")
        for second in range(1, video.duration + 1):
            time.sleep(1)
            print(second, end=' ')
        print("Конец видео.")
        video.time_now = 0


print(introspection_info(UrTube))