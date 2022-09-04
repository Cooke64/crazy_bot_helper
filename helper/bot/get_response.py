from typing import Union, List, Tuple

import requests
from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from requests import Response


async def send_error_message(message: types.Message):
    await message.answer(
        'Я тебя не понял. Введи Помощь '
        'или /help, чтобы узнать порядок работы с ботом'
    )


def create_subscribe_menu(
        country_pk: int, user_id: int) -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    response = subscribe_country(country_pk, user_id, method='get')
    if response.status_code == 201:
        message_to_user, func = 'Отписаться', 'delete_fave'
    else:
        message_to_user, func = 'Подписаться', 'get_in_fave'
    keyboard.add(
        types.InlineKeyboardButton(
            text="Назад",
            one_time_keyboard=True,
            callback_data="get_back",
        ),
        types.InlineKeyboardButton(
            text=message_to_user,
            one_time_keyboard=True,
            callback_data=func
        )
    )
    return keyboard


def get_data_to_country_pk(request_data: dict) -> Tuple[str, int]:
    try:
        data = request_data['results'][0]
        result_data = print_response(data)
        if isinstance(data, dict):
            country_pk = data['pk']
            return result_data, country_pk
        else:
            raise 'переменная data не является словарем'
    except KeyError as e:
        raise e
    except IndexError as e:
        raise e


def make_keyboard(data_to_keyboard: List[List[str]]) -> InlineKeyboardMarkup:
    __keyboard = types.InlineKeyboardMarkup()
    for rows in data_to_keyboard:
        btn = types.InlineKeyboardButton(
            callback_data=rows[0],
            text=rows[1],
        )
        __keyboard.insert(btn)
    return __keyboard


class Responser:
    BASE = 'http://127.0.0.1:8000/api/'

    def __init__(self):
        self.methods = {'get': requests.get, 'post': requests.post,
                        'delete': requests.delete}

    def __get_urls(self, url, message: types.Message = None,
                   call: types.CallbackQuery = None):
        if message:
            user_id = message.from_user.id
            country = message.text.title()
        else:
            user_id = call.from_user.id
            country = ''
        __urls = {
            'send_response': self.BASE + f'country/?name={country}',
            'get_last_seen': self.BASE + f'country/{user_id}',
            'get_favorite': self.BASE + f'favorites/{user_id}/get_list/',
            'register_user': self.BASE + 'users/',
            'delete_profile': self.BASE + f'users/{user_id}/delete',
            'find_user': self.BASE + f'users/{user_id}/subscribe/'
        }
        return __urls[url]

    def get_handler(self, url: str, message: types.Message = None,
                    call: types.CallbackQuery = None, method=None,
                    status_code: bool = False) -> Union[bool, dict]:
        """
        Обрабатывает get запросы.
        :param url: ссылка, указывается по названию функции.
        :param message: объект types.Message.
        :param call: объект types.CallbackQuery.
        :param method: деволтное значение get
        :param status_code: дефолтное значение False
        :return: Возвращает статус код, если True, иначе json ответ
        """
        action = self.methods[method if method else 'get']
        data = self.__get_urls(url, message, call)
        response = action(data)
        return response.status_code == 200 if status_code else response.json()

    def action_handler(self, url: str, message: types.Message,
                       method: str = 'post'):
        """
        Метод для обработки post и delete запросов
        :param url: по названию функции, где она вызывается
        :param message: types.Message
        :param method: дефолтный метод post
        :return: статус код запроса
        """
        chat_id = message.from_user.id
        username = message.from_user.username
        url = self.__get_urls(url, message)
        data = {'chat_id': chat_id, 'username': username}
        action = self.methods[method]
        response = action(url=url, data=data if data else None)
        return response.status_code

    def get_simple_request(self, url):
        data = self.methods['get'](url=url)
        return data.json()


def print_response(data: dict) -> str:
    response_message = ''
    response_message += f"<b>{data['name']}</b>\n"
    friend = 'нашими кентами' if data['is_friendly'] else 'врагом'
    response_message += f"<b>Страна является {friend}</b> \n"
    for i in data['moving_order']:
        message = ''
        message += f"<b>{i['name']}</b> \n"
        message += f"{i['visa_info']} \n"
        message += '---' * 20 + '\n'
        response_message += message
    return response_message


def make_data_and_keyboard(message, request_data):
    data, country_pk = get_data_to_country_pk(request_data)
    user_id = message.from_user.id
    keyboard = create_subscribe_menu(
        country_pk=country_pk,
        user_id=user_id
    )
    requests.post(
        url=f'http://127.0.0.1:8000/api/country/{country_pk}/{user_id}/',
    )
    return data, keyboard


def subscribe_country(pk: int, user_id: int, method: str) -> Response:
    d = {'post': requests.post, 'delete': requests.delete, 'get': requests.get}
    response = d[method](
        url=f'http://127.0.0.1:8000/api/country/{pk}/subs/{user_id}/',
    )
    return response


def get_country_doc(country_name: str, document_name: list) -> dict:
    document_name = '+'.join(document_name)
    url = f'http://127.0.0.1:8000/api/documents/?country__name={country_name}&document__name={document_name}'
    response = requests.get(
        url=url,
    )
    return response.json()


def print_response_country_doc(data: dict) -> str:
    response_message = ''
    for i in data[0].values():
        response_message += f'{i} \n'
    return response_message
