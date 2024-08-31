import pandas as pd
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram import F, Router

import app.keyboards as kb
from app.DatabaseProvider.provider import ProviderDb
from app.StatesModels.Account.authUserDto import AuthUserDto
from app.Resources.texts.namings import admin, tech_support, moderator, user, director_sn

router = Router()
context = ProviderDb()

register_role = {
    admin: [],
    tech_support: [],
    moderator: [],
    user: [],
    director_sn: [],
}

users_ids = {}


def delete_register_role(value):
    print(register_role)
    key = get_register_role(value)
    register_role[key].remove(value)


def get_register_role(user_id: int):
    for key, value in register_role.items():
        if user_id in value:
            return key

    return None


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать в мини социальную сеть! Требуется выбрать роль', reply_markup=kb.mainButtons)
    print(message.chat.id)


@router.message(F.text.in_([admin, tech_support, moderator, user, director_sn]))
async def choose_role(message: Message, state: FSMContext):
    # отдельный алгоритм для роли пользователя(он участвует в базе данных)
    if message.text == user:
        await state.set_state(AuthUserDto.name)
        await message.reply("Введите свою Фамилию и Имя (или наоборот) для входа")
    else:
        # регистрация роли во временное хранилище (словарь)
        register_role[message.text].append(message.from_user.id)
        context.set_connection(get_register_role(message.from_user.id))

        print(f"{message.text}: ", register_role[message.text])
        await message.answer("Выберите, с чем вы хотите работать", reply_markup=kb.first_part_tables)


@router.message(F.text == "Еще -->")
async def choose_entities_more(message: Message):
    await message.reply("Выберите, с чем вы хотите работать", reply_markup=kb.second_part_tables)


@router.message(F.text == "<-- Назад")
async def choose_entities_back(message: Message):
    await message.reply("Выберите, с чем вы хотите работать", reply_markup=kb.first_part_tables)


@router.message(F.text == "Выход")
async def exit_button(message: Message):
    delete_register_role(message.from_user.id)

    if message.from_user.id in users_ids.keys():
        users_ids.pop(message.from_user.id)

    await message.reply("Выход", reply_markup=kb.mainButtons)


@router.callback_query(F.data == "back")
async def back_button(call: CallbackQuery):
    await call.message.answer("Выберите, с чем вы хотите работать", reply_markup=kb.first_part_tables)


@router.message(F.text == "Отменить")
async def cancel_button(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите, с чем вы хотите работать", reply_markup=kb.first_part_tables)


async def CRUD_button_with_table(message: Message, df: pd.DataFrame, table_name: str):
    if df.empty:
        await df_empty(df, message)
    else:
        await answer_dataframe(df, message)

    await message.answer(
        "Выберите вариант",
        reply_markup=kb.create_inline_keyboard(table_name, get_register_role(message.chat.id)))

    msg = await message.answer("_", reply_markup=ReplyKeyboardRemove())
    await msg.delete()


async def df_empty(df: pd.DataFrame, message: Message):
    await message.reply("<b>Таблица пустая ⚠️</b>", parse_mode="HTML")


async def answer_dataframe(df: pd.DataFrame, message: Message):

    df_mark = df.to_markdown()
    if len(df_mark) > 4096:
        for x in range(0, len(df_mark), 4096):
            await message.answer(text=f"<pre>{df_mark[x:x+4096]}</pre>", parse_mode="HTML")
    else:
        await message.answer(text=f"<pre>{df_mark}</pre>", parse_mode="HTML")
