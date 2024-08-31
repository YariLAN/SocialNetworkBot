import pandas as pd
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery
from matplotlib import pyplot as plt

import app.keyboards as kb
from app.Handlers.messages_handlers import inline_users
from app.Repositories.messageRepository import MessageRepository
from app.Repositories.groupsRepository import GroupsRepository
from app.Resources.texts.namings import d_ent_func
from app.StatesModels.Group.getFriendGroupsDto import GetFriendGroupsDto
from app.handlers import df_empty, answer_dataframe
from settings import path_images

router = Router()


@router.message(F.text == d_ent_func[2])
async def create_func_groups_keyboard(message: Message):
    await message.delete()
    await message.answer("Список функций", reply_markup=kb.additional_groups_buttons)


@router.message(F.text == "Список групп друзей пользователя")
async def get_friend_groups(message: Message, state: FSMContext):
    await state.set_state(GetFriendGroupsDto.account_id)
    await message.answer("Выберите пользователя", reply_markup=await inline_users())


@router.callback_query(GetFriendGroupsDto.account_id)
async def get_friend_groups_account_id(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(account_id=callback_query.data)
    data = await state.get_data()
    await state.clear()

    df = await GroupsRepository.getFriendGroups(int(data["account_id"]))

    if df.empty:
        await df_empty(df, callback_query.message)
    elif 'Exception' in df.columns:
        await answer_dataframe(df, callback_query.message)
    else:
        await answer_dataframe(df, callback_query.message)


@router.message(F.text == "Зал с максимальной наполняемостью")
async def get_hall_with_max_occupancy(message: Message):
    df = await GroupsRepository.GetHallWithMaxOccupancy()

    if df.empty:
        await df_empty(df, message)
    else:
        await answer_dataframe(df, message)


async def show_histogram(message: Message, df: pd.DataFrame):
    titles = [row.title for row in df.itertuples()]
    tickets_sold = [row.tickets_sold for row in df.itertuples()]

    plt.figure(figsize=(10, 6))
    plt.bar(titles, tickets_sold, color='blue')
    plt.xlabel('Фильмы')
    plt.ylabel('Проданные билеты')
    plt.title('Распределение количества проданных билетов по фильмам')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    png = path_images + "get_sold_tickets_by_film.png"
    plt.savefig(png, dpi=300)

    await message.answer_photo(
        caption=f'Распределение количества проданных билетов по фильмам',
        photo=FSInputFile(path=png))


@router.message(F.text == "Количество проданных билетов по фильмам")
async def get_sold_tickets_by_film(message: Message):
    df = await MessageRepository.getSoldTicketsByFilms()

    if df.empty:
        await df_empty(df, message)
    elif "Exception" in df.columns:
        await answer_dataframe(df, message)
    else:
        await show_histogram(message, df)


@router.message(F.text == "Ежедневный доход от продажи билетов")
async def get_sold_daily_revenue_by_sold_tickets(message: Message):
    df = await SoldTicketsRepository.getDailyRevenue()

    if df.empty:
        await df_empty(df, message)
    elif "Exception" in df.columns:
        await answer_dataframe(df, message)
    else:
        await show_line_chart(message, df)


async def show_line_chart(message: Message, df: pd.DataFrame):
    dates = [row.sale_date for row in df.itertuples()]
    daily_revenue = [row.daily_revenue for row in df.itertuples()]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, daily_revenue, marker='o', linestyle='-')
    plt.xlabel('Дата')
    plt.ylabel('Ежедневный доход')
    plt.title('Ежедневный доход от продажи билетов')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    png = path_images + "get_sold_daily_revenue_by_sold_tickets.png"
    plt.savefig(png, dpi=300)

    await message.answer_photo(
        caption=f'Ежедневный доход от продажи билетов',
        photo=FSInputFile(path=png))


