from app.Repositories.baseRepository import BaseRepository


class FriendsRepository:

    @staticmethod
    async def getAll():
        return await BaseRepository.get_query("SELECT * FROM friends")

    @staticmethod
    async def getByFriendId(user_id: int):
        return await BaseRepository.get_query(f"SELECT * FROM friends Where account_id = {user_id}")

    @staticmethod
    async def getByUserId(user_id: int):
        return await BaseRepository.get_query(f"CALL GetFriends('{user_id}')")

    @staticmethod
    async def getMostFriendlyResident():
        return await BaseRepository.get_query(f"CALL MostFriendlyResident()")

    @staticmethod
    async def add(account_id: int, friend_id: int):
        return await BaseRepository.add_query(f"INSERT INTO friends VALUES (NULL, {account_id},  {friend_id})")

    @staticmethod
    async def getCountFriends():
        return await BaseRepository.get_query("""
            SELECT a.Fullname, COUNT(d.account_id) as Количество_друзей
            FROM accounts a
            LEFT JOIN friends d ON a.id = d.account_id
            GROUP BY a.id, a.Fullname
            """)
