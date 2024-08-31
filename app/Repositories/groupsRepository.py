import app.DatabaseProvider.provider as provider
import pandas as pd

from app.Repositories.baseRepository import BaseRepository


class GroupsRepository:

    @staticmethod
    async def getAll():
        return await BaseRepository.get_query("SELECT * FROM social_network.`groups`")

    async def get(id: int):
        return await BaseRepository.get_query(f"SELECT * FROM social_network.`groups` WHERE id= {id}")

    @staticmethod
    async def getFriendGroups(user_id: int):
        return await BaseRepository.get_query(f"CALL GetFriendGroups({user_id})")    \

    @staticmethod
    async def GetHallWithMaxOccupancy():
        return await BaseRepository.get_query(f"CALL GetHallWithMaxOccupancy()")
