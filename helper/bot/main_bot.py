import logging

from aiogram import Bot, Dispatcher, executor, types

from bot import markups
from bot.get_response import subscribe_country, get_country_doc, \
    print_response_country_doc, Responser, make_data_and_keyboard, \
    send_error_message, make_keyboard

TOKEN = '5789236771:AAE-a4HZXEerjkcgeFGMwVEUrk0tFFhDZxw'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)
responser = Responser()


async def send_response(message: types.Message, url: str = None) -> None:
    """
    Обрабатывает пользовательские запросы, написанные
     самостоятельно с клавиатуры
    Функция create_subscribe_menu формирует меню подписаться\отписаться
    в зависимости от запроса, который показывает, есть ли в подписках данный объект
    :param message: types.Message
    :param url: При обработке запросов по прямому url
    передается ссылка, а не параметры
    :return: возвращает сообщение пользователю.
    """
    if not url:
        request_data = responser.get_handler(
            url='send_response', message=message
        )
    else:
        request_data = responser.get_simple_request(url)
    if request_data:
        try:
            data, keyboard = make_data_and_keyboard(message, request_data)
            await message.answer(data, reply_markup=keyboard)
        except IndexError:
            await send_error_message(message)


@dp.callback_query_handler(text="get_back")
async def get_back(call: types.CallbackQuery, ):
    await call.answer(text="Спасибо, что воспользовались ботом!",
                      show_alert=True)
    await get_country(call.message)


@dp.callback_query_handler(text="delete_fave")
async def del_from_fav(call: types.CallbackQuery, ):
    last = responser.get_handler(url='get_last_seen', call=call)
    resp = subscribe_country(
        pk=int(*last),
        user_id=call.from_user.id,
        method='delete'
    )
    await call.answer(resp.text)


@dp.callback_query_handler(text="get_in_fave")
async def get_in_fav(call: types.CallbackQuery, ):
    """
    last -  получаем последнюю просмотренный объект,
    который можно добавить в избранное. Делает два запроса:
    на получение объекта и создание, если такого нет.
    """
    last = responser.get_handler(url='get_last_seen', call=call)
    resp = subscribe_country(
        pk=int(*last),
        user_id=call.from_user.id,
        method='post'
    )
    await call.answer(resp.text)


async def register_user(message: types.Message):
    status = responser.action_handler(message=message, url='register_user')
    response = f'Вы зарегистрированы' if status == 201 else 'Вы уже зарегистрированы'
    await message.answer(response)


async def delete_profile(message: types.Message):
    responser.action_handler(
        message=message, url='delete_profile', method='delete'
    )
    await message.answer('Пользователь удален', )


@dp.callback_query_handler(text="get_back")
async def get_back(call: types.CallbackQuery, ):
    await get_country(call.message)


@dp.callback_query_handler()
async def func(call: types.CallbackQuery, ):
    await send_response(call.message, url=call.data)


async def get_favorite(message: types.Message):
    request_data = responser.get_handler(message=message, url='get_favorite')
    response = request_data['results']
    data = [[i['url'], i['country_name'], i['country_pk']] for i in response]
    markup = make_keyboard(data)
    mes = 'Вы ничего не добавили в избранное' if not response else 'Ваши избранные страны'
    await message.answer(mes, reply_markup=markup)


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if responser.get_handler(
            message=message,
            url='find_user',
            status_code=True
    ):
        markup.add(*markups.BUTTONS_REG)
    else:
        markup.add(*markups.BUTTONS)
    await message.answer(
        f'<b>Привет, {message.from_user.first_name}. Чем помочь? </b>',
        reply_markup=markup
    )


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await message.answer(markups.HELP_MESSAGE)


@dp.message_handler(content_types=['text,'])
async def get_info_subscription(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*markups.BUTTONS_SUBSCRIBE)
    await message.answer(
        markups.INFO_SUBSCRIPTION,
        reply_markup=markup
    )


@dp.message_handler(content_types=['text,'])
async def get_country(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*markups.COUNTRY_BUTTONS)
    await message.answer(
        '<b>Что ищем?</b>',
        reply_markup=markup
    )


commands = {
    'Помощь': help_message,
    'Старт': start_bot,
    'Узнать страну': get_country,
    'Назад': start_bot,
    'Зарегистрироваться': register_user,
    'Порядок пересечения': send_response,
    'Удалить профиль': delete_profile,
    'Узнать про подписку': get_info_subscription,
    'Избранное': get_favorite
}


async def get_response_doc(message: types.Message):
    country_name, *document_name = message.text.split()
    response = get_country_doc(country_name, document_name)
    if response:
        message_to_show = print_response_country_doc(response)
        await message.answer(message_to_show)


@dp.message_handler(content_types=['text'])
async def get_user_message(message):
    command = message.text
    # Исправить этот костыль!!!
    if len(command.split()) == 3 and 'Узнать' not in command:
        await get_response_doc(message)
    elif command in commands:
        await commands[command](message)
    else:
        await send_response(message)


executor.start_polling(dp, skip_updates=True)
