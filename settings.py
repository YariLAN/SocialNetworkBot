import os

path_images = os.environ.get('PATH_IMAGES', 'app/Resources/images/')

users = {
    "Тех. поддержка": {'name': 'tech_support', 'password': 'password'},
    'Администратор БД': {'name': 'root', 'password': 'SuaiYarik281_'},
    'Модератор': {'name': 'moderator', 'password': 'password'},
    'Пользователь': {'name': 'user', 'password': 'password'},
    'Директор': {'name': 'director_sn', 'password': 'password'}
}

rights_role = {
    'Тех. поддержка': ["accounts", "messages"],
    'Модератор': ["accounts", "groups", "messages"],
    'Пользователь': ["groups", "friends", "messages", "accounts"],
    'Директор': ["subscriptions"],
}

