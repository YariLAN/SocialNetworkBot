from aiogram.fsm.state import StatesGroup, State


class GetFriendsDto(StatesGroup):
    account_id = State()
