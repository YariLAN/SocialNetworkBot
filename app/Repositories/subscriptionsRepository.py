from app.Repositories.baseRepository import BaseRepository


class SubscriptionsRepository:

    @staticmethod
    async def getAll():
        return await BaseRepository.get_query("SELECT * FROM subscriptions")

    @staticmethod
    async def update(session_id: int, field_name: str, value: str) -> bool:
        res = await BaseRepository.update_query(
            f"UPDATE sessions SET {field_name} = '{value}' WHERE session_id = {session_id}")

        return res

    @staticmethod
    async def getSuggestGroupFriendsForAllResidents():
        return await BaseRepository.get_query(f"CALL SuggestGroupFriendsForAllResidents()")

    @staticmethod
    async def getAverageAgeInGroup(group_id: int):
        return await BaseRepository.get_query(f"CALL GetAverageAgeInGroup('{group_id}')")

    @staticmethod
    async def getAverageAgeInGroups():
        return await BaseRepository.get_query("""
            SELECT g.Name as Название, AVG(a.Age) as Средний_возраст
            FROM accounts a
            JOIN subscriptions gr ON a.id = gr.account_id
            JOIN social_network.`groups` g ON gr.group_id = g.id
            GROUP BY g.Name""")
