tech_support, admin, moderator, user, director_sn = [
    "Тех. поддержка",
    "Администратор БД",
    "Модератор",
    "Пользователь",
    "Директор"]

d_action = {
    "Добавить ➕": "add",
    "Удалить ❌": "del",
    "Изменить ✏️": "edit",
    "Показать 👀": "show",
    "Список 👀📋": "list"}

d_ent_func = [
    "Друзья 🎅",
    "Аккаунты 🛠️",
    "Группы 🔧",
    "Сообщения ✍️",
    "Подписчики групп 👥"]


class TableNames(object):
    accounts: str = "accounts",
    groups: str = "groups",
    subscriptions: str = "subscriptions",
    messages: str = "messages",
    friends: str = "friends",
