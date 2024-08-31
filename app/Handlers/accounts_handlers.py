from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import app.keyboards as kb
from app.Repositories.accountsRepository import AccountsRepository
from app.StatesModels.Account.authUserDto import AuthUserDto
from app.handlers import CRUD_button_with_table, users_ids, register_role, context
from app.Resources.texts.namings import TableNames, user

router = Router()


@router.message(F.text == "Аккаунты")
async def getCashiers(message: Message):
    df = await AccountsRepository.getAll()

    df.set_index('id', inplace=True)

    await CRUD_button_with_table(message, df, "accounts")


@router.message(AuthUserDto.name)
async def auth_cashier_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    context.set_connection(user)
    await state.clear()

    names = message.text.split(" ")
    df = await AccountsRepository.getByName(names[0], names[1])

    if df.empty:
        await message.reply("<b>Такого пользователя не существует ⚠️</b>", parse_mode="HTML")
        return

    users_ids[message.from_user.id] = df["id"].values[0]
    register_role[user].append(message.from_user.id)

    print(f"{user}: ", register_role[user])
    await message.reply("<b>Вы успешно вошли как пользователь сети</b>", parse_mode="HTML")
    await message.answer("Выберите, с чем вы хотите работать", reply_markup=kb.first_part_tables)
