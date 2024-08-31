from aiogram.fsm.state import StatesGroup, State


class CreateFriendsDto(StatesGroup):
    account_id = State()
    friend_id = State()
