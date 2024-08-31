from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.Resources.texts.namings import admin, tech_support, moderator, user, d_action, d_ent_func, director_sn
from settings import rights_role

mainButtons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=admin)],
    [KeyboardButton(text=moderator), KeyboardButton(text=director_sn)],
    [KeyboardButton(text=tech_support), KeyboardButton(text=user)]],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню...")

first_part_tables_buttons = [
    [KeyboardButton(text="Аккаунты"), KeyboardButton(text="Друзья")],
    [KeyboardButton(text="Группы"), KeyboardButton(text="Подписчики групп")],
    [KeyboardButton(text="Сообщения")],
    [KeyboardButton(text="Выход"), KeyboardButton(text="Еще -->")]]

second_part_tables_buttons = [
    [KeyboardButton(text="Дополнительные функции")],
    [KeyboardButton(text="<-- Назад")]]

additional_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=d_ent_func[0]), KeyboardButton(text=d_ent_func[1])],
    [KeyboardButton(text=d_ent_func[2]), KeyboardButton(text=d_ent_func[3])],
    [KeyboardButton(text=d_ent_func[4])],
    [KeyboardButton(text="<-- Назад")]],
    resize_keyboard=True)

# Друзья
additional_friends_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Список друзей пользователя')],
    [KeyboardButton(text='Дружелюбный пользователь')],
    [KeyboardButton(text='Кол-во друзей у топ-10 пользователей')],  # Диаграмма
    [KeyboardButton(text="Назад")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите запрос")

# Группы
additional_groups_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Список групп друзей пользователя")],
    [KeyboardButton(text="Назад")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите запрос")

# Аккаунты
additional_accounts_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Большая разница в возрасте")],  # FindMaxAgeDifference
    [KeyboardButton(text="Пользователь, создавший большех всех групп")],  # FindTopGroupCreator
    [KeyboardButton(text="Список влиятельных пользователей - создателей групп")],  # GetInfluentialUsers
    [KeyboardButton(text="Самые молодые пользователи")],  # GetYoungestUsers
    [KeyboardButton(text="Распределение возрастов")],  # GetYoungestUsers
    [KeyboardButton(text="Назад")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите запрос")

# Сообщения
additional_messages_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Список сообщений пользователя")],  # GetUserMessages(user_id: int)
    [KeyboardButton(text="Назад")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите запрос")

# Подписчики
additional_subscribers_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Предложения друзей пользователя на основе общ. групп")], # SuggestGroupFriendsForAllResidents
    [KeyboardButton(text="Ср. возраст участников определенной группы")],  # GetAverageAgeInGroup(group_id)
    [KeyboardButton(text="Ср. возраст участников каждой группы")],  # GetAverageAgeInGroup(group_id)
    [KeyboardButton(text="Назад")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите запрос")

first_part_tables = ReplyKeyboardMarkup(keyboard=first_part_tables_buttons,
                                        resize_keyboard=True,
                                        input_field_placeholder="Выберите пункт меню...")

second_part_tables = ReplyKeyboardMarkup(keyboard=second_part_tables_buttons,
                                         resize_keyboard=True,
                                         input_field_placeholder="Выберите пункт меню...")

cancel_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отменить")]], resize_keyboard=True)


# Кнопки для выбора из категорий
async def set_inline_buttons_from_db(entities):
    buttons = []
    for item in entities:
        buttons.append(InlineKeyboardButton(text=item.name, callback_data=item.id))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def create_reply_keyboard(entity):
    keyboard = ReplyKeyboardBuilder()

    for action in ["Добавить", "Удалить", "Изменить", "Показать"]:
        keyboard.add(KeyboardButton(text=f"{action} {entity}", callback_data=action))
    keyboard.add(KeyboardButton(text="Список всех"))
    keyboard.add(KeyboardButton(text="Вернуться к другим данным"))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)


def create_inline_keyboard(table_name: str, role: str):
    keyboard = InlineKeyboardBuilder()

    # если роль админа или таблица входит в права другой роли
    if role == admin or table_name in rights_role[role]:
        buttons = d_action.keys()
    else:
        buttons = list(d_action.keys())[3:5]

    for key in buttons:
        keyboard.add(InlineKeyboardButton(text=key, callback_data=f"{table_name}_{d_action[key]}"))

    keyboard.add(InlineKeyboardButton(text="Вернуться к другим данным", callback_data="back"))

    return keyboard.adjust(2).as_markup()


def create_keyboard():
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(KeyboardButton(text="Вернуться к другим данным"))

    return keyboard.as_markup(resize_keyboard=True)


back_button = create_keyboard()
