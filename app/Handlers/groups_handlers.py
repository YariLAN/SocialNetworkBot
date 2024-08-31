from aiogram import F, Router
from aiogram.types import Message

from app.Repositories.groupsRepository import GroupsRepository

from app.handlers import CRUD_button_with_table

router = Router()


@router.message(F.text == "Группы")
async def getHalls(message: Message):
    df = await GroupsRepository.getAll()
    await CRUD_button_with_table(message, df, "groups")