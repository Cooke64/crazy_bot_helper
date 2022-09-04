from telebot import types


BUTTONS = {
    'Помощь': types.KeyboardButton('Помощь'),
    'Старт': types.KeyboardButton('Старт'),
    'Узнать страну': types.KeyboardButton('Посмотреть страну'),
    'Зарегистрироваться': types.KeyboardButton('Зарегистрироваться'),
}

BUTTONS_REG = {
    'Помощь': types.KeyboardButton('Помощь'),
    'Старт': types.KeyboardButton('Старт'),
    'Узнать страну': types.KeyboardButton('Посмотреть страну'),
    'Удалить профиль': types.KeyboardButton('Удалить профиль'),
    'Узнать про подписку': types.KeyboardButton('Узнать про подписку'),
}

COUNTRY_BUTTONS = {
    'Порядок пересечения': types.KeyboardButton('Порядок пересечения'),
    'Виды документов': types.KeyboardButton('Виды документов'),
    'Информация о стране': types.KeyboardButton('Информация о стране'),
    'Назад': types.KeyboardButton('Назад'),
}

BUTTONS_SUBSCRIBE = {
    'Избранное': types.KeyboardButton('Избранное'),
    'Отписаться': types.KeyboardButton('Отписаться'),
    'Назад': types.KeyboardButton('Назад')
}

HELP_MESSAGE = f"""<b>Как это работает?!</b> \n
Вводишь <b>страну</b>, получаешь порядок пересечения\n
Вводишь <b>страну и вид документа</b> через <b>пробел</b>, получаешь порядок пересечения по данному документы\n'
Вводишь страну и документ и получаешь пизды\n
"""

INFO_SUBSCRIPTION = """
Нажми на кнопку подписаться и получишь эксклюзивный контент о странах и прочей херне
"""
