from aiogram.fsm.state import StatesGroup, State


class GetFriendGroupsDto(StatesGroup):
    account_id = State()