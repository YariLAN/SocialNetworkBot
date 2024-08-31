import pandas as pd
import pymysql

# from app.DatabaseProvider import provider


from app.handlers import context


class BaseRepository:
    @staticmethod
    async def get_query(sql: str):
        try:
            connect = context.connection
            with connect.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()

                return pd.DataFrame(result)
        except Exception as e:
            print("Ошибка при получении. Запрос: ", sql, "\nОшибка:", e)
            return None

    @staticmethod
    async def add_query(sql: str):
        try:
            connect = context.connection
            with connect.cursor() as cursor:

                cursor.execute(sql)
                connect.commit()
                return True
        except Exception as e:
            print("Ошибка при добавлении. Запрос: ", sql, "\nОшибка:", e)
            return f"Ошибка при добавлении: {e}"

    @staticmethod
    async def update_query(sql: str):
        try:
            connect = context.connection
            with connect.cursor() as cursor:

                cursor.execute(sql)
                connect.commit()
                return True
        except Exception as e:
            print("Ошибка при обновлении. Запрос: ", sql, "\nОшибка:", e)
            return False
