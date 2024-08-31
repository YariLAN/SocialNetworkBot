from aiogram.fsm.state import StatesGroup, State


class GetUserMessagesDto(StatesGroup):
    account_id = State()
