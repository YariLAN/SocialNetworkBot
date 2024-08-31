from aiogram.fsm.state import StatesGroup, State


class GetAverageAgeInGroup(StatesGroup):
    group_id = State()
