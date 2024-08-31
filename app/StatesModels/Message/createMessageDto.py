from aiogram.fsm.state import StatesGroup, State


class CreateMessageDto(StatesGroup):
    sender_id = State()
    recipient_id = State()
    text = State()
