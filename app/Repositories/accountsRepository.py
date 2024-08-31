from app.Repositories.baseRepository import BaseRepository


class AccountsRepository:

    @staticmethod
    async def getAll():
        return await BaseRepository.get_query("SELECT * FROM accounts")

    @staticmethod
    async def getById(id: int):
        return await BaseRepository.get_query(f"SELECT * FROM accounts WHERE id = '{id}'")

    @staticmethod
    async def getByName(lastName, firstName):
        return await BaseRepository.get_query(
            f"SELECT * FROM accounts "
            f"WHERE "
            f"Fullname = '{lastName} {firstName}' OR Fullname = '{firstName} {lastName}'")

    @staticmethod
    async def getFindMaxAgeDifference():
        return await BaseRepository.get_query("CALL FindMaxAgeDifference()")

    @staticmethod
    async def getFindTopGroupCreator():
        return await BaseRepository.get_query("CALL FindTopGroupCreator()")

    @staticmethod
    async def getInfluentialUsers():
        return await BaseRepository.get_query("CALL GetInfluentialUsers()")

    @staticmethod
    async def getYoungestUsers():
        return await BaseRepository.get_query("CALL GetYoungestUsers()")

    @staticmethod
    async def getAges():
        return await BaseRepository.get_query("SELECT Age FROM accounts")


