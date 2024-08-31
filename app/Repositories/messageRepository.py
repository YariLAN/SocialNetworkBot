from app.DbModels.Message import Message
from app.Repositories.baseRepository import BaseRepository
from app.handlers import context


class MessageRepository(object):

    @staticmethod
    async def getAll():
        return await BaseRepository.get_query("SELECT * FROM messages")

    @staticmethod
    async def getById(id: int):
        return await BaseRepository.get_query(f"SELECT * FROM messages Where id ={id}")

    @staticmethod
    async def getUserMessages(account_id: int):
        return await BaseRepository.get_query(f"CALL GetUserMessages('{account_id}')")

    @staticmethod
    async def add(message: Message):
        connect = context.connection

        try:
            with connect.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO {message.__tableName__} VALUES (NULL, %s, %s, %s, %s)",
                    (message.sender_id, message.recipient_id, message.text, message.date_message))

                connect.commit()
                return True

        except Exception as e:
            print("Ошибка при добавлении сообщения", e)
            return False
