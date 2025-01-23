from typing import Optional

import pytest
import requests
from Auth.AuthJson import json_for_api_version
from BaseDirectory.BaseModule import main_api_url, test_chat_hash, main_headers
from ChatGet.ChatGetJson import json_for_get_chat, json_for_topic_list, json_for_over_limit, \
    json_for_syncronization_direct_chats, json_for_syncronization_all_chats, ChatGetJson
from User.UserRequests import User


class ChatGet(User):

    def sychronistaion_list_count(self, count, request):
        x = 0
        while x < count:
            try:
                assert request.json()["response"]["updated"][x]["hash"]
                x = x + 1
            except IndexError:
                print(f"Список возвращаемых хэшей : {x}")
                assert x <= 100  # Проверка, что список обновленных чатов не может быть выше 100
                break
    def chat_information(self):
        """Корректный запрос"""
        chat_request = requests.get(f"{main_api_url}/chat/{test_chat_hash}", headers=main_headers, json=json_for_get_chat)
        assert chat_request.status_code == 200
        assert chat_request.json()["response"]["type"] == "private"
        """Неккоректный запрос(Пустые хедеры/Нет авторизации)"""
        no_auth_chat_request = requests.get(f"{main_api_url}/chat/{test_chat_hash}", json=json_for_get_chat)
        assert no_auth_chat_request.status_code == 401
        assert no_auth_chat_request.json()["errMsg"] == "NOT_FOUND_AUTH"
        """Неккоректный запрос(Отсутствует хэш чата)"""
        no_hash_chat_request = requests.get(f"{main_api_url}/chat/", headers=main_headers)
        print(no_hash_chat_request.json())
        assert no_hash_chat_request.status_code == 404
        assert no_hash_chat_request.json()["errMsg"] == "Not found method"

    def popular_chats(self):
        """Корректный запрос"""
        popular_chat_request = requests.get(f"{main_api_url}/chat/popular", headers=main_headers, json=json_for_api_version)
        first_chat_sort = popular_chat_request.json()["response"]["items"][0]["sort"]
        second_chat_sort = popular_chat_request.json()["response"]["items"][1]["sort"]
        """Проверка корректной сортировки чатов в ответе бэка"""
        def sorting_check():
            print(popular_chat_request.json())
            x = 0
            while x < 9:
                assert popular_chat_request.json()["response"]["items"][x]["sort"] >= \
                       popular_chat_request.json()["response"]["items"][x + 1]["sort"]
                x = x + 1
        """Проверка неккоректного запроса(Нет заголовков)"""
        no_auth_popular_chat_request = requests.get(f"{main_api_url}/chat/popular", json=json_for_api_version)
        assert no_auth_popular_chat_request.status_code == 401
        assert no_auth_popular_chat_request.json()["errMsg"] == "NOT_FOUND_AUTH"
        """Проверка Пустого JSON или неуказания версии API(Тест должен пройти с 200-ым ответом)"""
        no_json_popular_chat_request = requests.get(f"{main_api_url}/chat/popular", headers=main_headers)
        assert no_json_popular_chat_request.status_code == 200
        sorting_check()


    def get_topic_list(self):
        """Корректный запрос"""
        topic_list = requests.get(f"{main_api_url}/chat/get/topic", headers=main_headers, json=json_for_topic_list)
        assert topic_list.status_code == 200
        """Проверка, что списков в ответе действительно 100(максимум)"""
        def topic_list_count(count):
            x = 0
            while x < count:
                assert topic_list.json()["response"]["items"][x]["hash"]
                x = x + 1
        topic_list_count(100)
        """Превышение поля limit в JSON"""
        over_limit_topic_list = requests.get(f"{main_api_url}/chat/get/topic", headers=main_headers, json=json_for_over_limit)
        assert over_limit_topic_list.status_code == 200
        with pytest.raises(IndexError):
            topic_list_count(101)
            pytest.fail("Список топиков больше 100")
        """Проверка неккоректного запроса(Нет заголовков/Нет авторизации"""
        no_auth_topic_list = requests.get(f"{main_api_url}/chat/get/topic", json = json_for_topic_list)
        assert no_auth_topic_list.status_code == 401
        assert no_auth_topic_list.json()["errMsg"] == "NOT_FOUND_AUTH"
        """Проверка неккоректного запроса(Нет входящих параметров)"""
        no_params_topic_list = requests.get(f"{main_api_url}/chat/get/topic", headers=main_headers)
        assert no_params_topic_list.status_code == 200

    def synchronization_direct_chats_list(self):
        """Корректный запрос"""
        direct_chats = requests.get(f"{main_api_url}/chat/get/direct", headers=main_headers, json=json_for_syncronization_direct_chats)
        self.sychronistaion_list_count(100, request=direct_chats)
        """Некорректный запрос(Нет заголовков/Авторизации"""
        no_auth_direct_chats = requests.get(f"{main_api_url}/chat/get/direct", json=json_for_syncronization_direct_chats)
        assert no_auth_direct_chats.status_code == 401
        assert no_auth_direct_chats.json()["errMsg"] == "NOT_FOUND_AUTH"
        """Неккоректный запрос(Нет JSON). Должен прийти пустой ответ"""
        no_json_direct_chats = requests.get(f"{main_api_url}/chat/get/direct", headers=main_headers)
        print(no_json_direct_chats.json())
        assert no_json_direct_chats.status_code == 200
        """Превышение лимита запрашиваемых чатов в JSON"""
        chats = requests.get(f"{main_api_url}/chat/get/direct", json=json_for_over_limit, headers=main_headers)
        self.sychronistaion_list_count(count=150, request=chats)


    def get_users_from_chat(self, status_code: Optional[int] = None,
                          headers: Optional[dict] = None,
                          chat_hash: Optional[str] = None,
                          not_in_contact: Optional[bool] = None
                          ):
        role_array = ["OWNER", "MEMBER", "ADMIN"]
        if status_code == 200:
            req = requests.get(f"{main_api_url}/chat/{chat_hash}/users", headers=headers,
                               json=ChatGetJson.json_for_get_users_in_chat(chat_hash=chat_hash, not_in_contact=not_in_contact))
            assert req.status_code == 200, "Запрос не работает"
            response_data = req.json()["response"]
            for role in response_data:
                assert role["role"] in role_array, "Статус пользователя возвращается некорректно"
            hashes = [item['hash'] for item in response_data]
            assert len(hashes) == len(set(hashes)), "Возвращаемые хэши должны быть уникальны и не должны дублироваться"
            for data_hash in response_data:
                user_hash = data_hash["hash"]
                user_status = self.get_user_profile(user_hash=user_hash, status_code=200, headers=headers)[0]
                if not_in_contact is True:
                    try:
                        assert user_status == [''], "Возвращается некорректный статус пользователя"
                    except AssertionError:
                        assert user_status == ''
                elif not_in_contact is False:
                    try:
                        assert user_status in [['FRIEND'], ['NONE'], [''],
                                               ['BOT']], "Возвращается некорректный статус пользователя"
                    except AssertionError:
                        assert user_status in ['FRIEND', 'NONE', '',
                                               'BOT'], "Возвращается некорректный статус пользователя"
                elif not_in_contact is None:
                    # При пустом параметре not_in_contact должны возвращаться пользователи из контактной книги
                    try:
                        assert user_status in [['FRIEND'], ['NONE'], [''],
                                               ['BOT']], "Возвращается некорректный статус пользователя"
                    except AssertionError:
                        assert user_status in ['FRIEND', 'NONE', '',
                                               'BOT'], "Возвращается некорректный статус пользователя"
            return [req.json()]
        elif status_code == 401:
            req = requests.get(f"{main_api_url}/chat/{chat_hash}/users", headers=None,
                               json=ChatGetJson.json_for_get_users_in_chat(chat_hash=chat_hash,
                                                                           not_in_contact=not_in_contact))
            assert req.status_code == 401, "Не возвращается ошибка при выполнении запроса без  авторизации"
            assert req.json()["errMsg"] == self.no_auth_error, "Не возвращается ошибка при выполнении запроса без авторизации"
        elif status_code == 404:
            # Запрос с пустым chat_hash
            req = requests.get(f"{main_api_url}/chat/{chat_hash}/users", headers=headers,
                               json=ChatGetJson.json_for_get_users_in_chat(chat_hash=None,
                                                                           not_in_contact=not_in_contact))
            assert req.status_code == 404, "Не возвращается ошибка в запросе, если он выполняется без хэша чата"
            assert req.json()["errMsg"] == self.not_found_methods_error, "Не возвращается ошибка в запросе, если он выполняется без хэша чата"





















