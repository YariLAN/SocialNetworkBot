import pymysql.cursors

from settings import users


class ProviderDb:
    connection = None

    def __init__(self):
        pass

    def set_connection(self, role: str):
        self.connection = pymysql.connect(
            host='localhost',
            user=users[role]['name'],
            password=users[role]['password'],
            db='social_network',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
