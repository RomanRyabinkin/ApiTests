from re import search

import pytest
import requests

from Search.SearchJson import SearchJson


class Search(SearchJson):
    def search_request(self, search_chat: bool, chat_hash: str = None):
        if search_chat == False:
            search_request = f"{self.main_api_url}/search"
        else:
            search_request = f"{self.main_api_url}/search/chat/{chat_hash}"
        return search_request

    def search(self, status_code: int, offset: int, s: str, limit: int, search_type: str):
        if status_code == 200:
            # Поиск только по Search Type
            search = requests.get(self.search_request(search_chat=False),
                                  headers=self.get_headers(self.main_user_token_url),
                                  json=self.search_json(s=s, offset=offset, limit=limit, search_type=search_type))
            assert search.status_code == 200, "Не работает запрос"
            if search_type == "CONTACT":
                try:
                    assert type(
                        search.json()["response"]["contacts"][0][
                            "hash"]) == str, "Юзер хэш передается в неккоректном формате"
                    assert len(search.json()["response"]["contacts"][0][
                                   "hash"]) == self.hash_length, "Неккоректная длина юзер хэша в ответе"
                    assert search.json()["response"]["contacts"][0]["avatar"].__contains__(
                        self.avatar_server_url), "Не передается аватарка в ответе"
                    full_name = self.full_test_user_name.split()
                    full_name_array = list(full_name)
                    name = full_name_array[0]
                    surname = full_name_array[1]
                    assert search.json()["response"]["contacts"][0]["name"] == name, "Не передается имя юзера в ответе"
                    assert search.json()["response"]["contacts"][0][
                               "surname"] == surname, "Не передается имя юзера в ответе"
                except KeyError:
                    # Если Limit > 50, проверяем ошибку
                    if limit > 50:
                        assert search.json()["errMsg"] == "limit, max 50", "Запрос работает при limit > 50"
            if search_type == "THREAD":
                x = 0
                while x < limit + 1:
                    try:
                        try:
                            assert search.json()["response"]["threads"][x]["message"].__contains__(
                                s), "Не передается текст треда в ответе"
                        except AssertionError:
                            assert search.json()["response"]["threads"][x]["message"].__contains__(
                                s.upper()), "Не передается текст треда в ответе"
                        assert type(search.json()["response"]["threads"][x][
                                        "id"]) == int, "Айди треда неккоректно передается в ответе"
                        assert type(search.json()["response"]["threads"][x][
                                        "hash"]) == str, "Хэш треда неккоректно возвращается в ответе"
                        assert len(search.json()["response"]["threads"][x][
                                       "hash"]) == self.hash_length, "Хэш должен быть длиной в 36 символов"
                        assert type(search.json()["response"]["threads"][x][
                                        "user_hash"]) == str, "Хэш пользователя неккоректно возвращается в ответе"
                        assert len(search.json()["response"]["threads"][x][
                                       "user_hash"]) == self.hash_length, "Хэш должен быть длиной в 36 символов"
                        assert type(search.json()["response"]["threads"][x][
                                        "subject_hash"]) == str, "Хэш треда неккоректно возвращается в треде"
                        assert len(search.json()["response"]["threads"][x][
                                       "user_hash"]) == self.hash_length, "Хэш должен быть длиной в 36 символов"
                        assert search.json()["response"]["threads"][x][
                                   "subject_type"] == "thread", "Неккоректно возвращается subject type"
                        assert type(search.json()["response"]["threads"][x][
                                        "parent_subject_hash"]) == str, "Parent Subject hash возвращается в неккоректном формате"
                        assert len(search.json()["response"]["threads"][x][
                                       "parent_subject_hash"]) == self.hash_length, "Хэш должен быть длиной в 36 символов"
                        x += 1
                    except IndexError:
                        assert x <= limit, "В ответе выдается больше сообщений, чем limit"
                        x += 1
                    except KeyError:
                        # Если limit > 50, Проверяем ошибку
                        if limit > 50:
                            assert search.json()["errMsg"] == "limit, max 50", "Запрос работает при limit > 50"
                        break
            elif search_type == "FILE":
                x = 0
                while x < limit + 1:
                    try:
                        assert type(
                            search.json()["response"]["files"][x]["id"]) == int, "Не выдается айди файла в ответе"
                        assert type(
                            search.json()["response"]["files"][x][
                                "created_at"]) == int, "Не выдается created_at в ответе"
                        assert type(
                            search.json()["response"]["files"][x]["size"]) == int, "Не выдается размер файла в ответе"
                        assert type(
                            search.json()["response"]["files"][x]["type"]) == str, "Не передает тип файла в ответе"
                        assert len(
                            search.json()["response"]["files"][x]["filename"]) != 0, "Не выдается имя файла в ответе"
                        assert search.json()["response"]["files"][x]["url"].__contains__(
                            self.files_server_url), "Не выдается урл файла в ответе"
                        x += 1
                    except IndexError:
                        assert x <= limit, "Выдало больше сообщений, чем limit"
                        x += 1
                    except KeyError:
                        # Если limit > 50, Проверяем ошибку
                        if limit > 50:
                            assert search.json()["errMsg"] == "limit, max 50", "Запрос работает при limit > 50"
                        break
            elif search_type == "MESSAGE":
                x = 0
                while x < limit + 1:
                    try:
                        assert search.json()["response"]["messages"][x][
                            "message"], "Не работает выдача сообщений в пределах limit"
                        x += 1
                    except IndexError:
                        assert x <= limit, "Выдало больше сообщений, чем limit"
                        x += 1
                    except KeyError:
                        # Если Limit > 50, проверяем ошибку
                        if limit > 50:
                            assert search.json()["errMsg"] == "limit, max 50", "Запрос работает при limit > 50"
                        break
            elif search_type == "ALL":
                x = 0
                while x < 50:
                    try:
                        assert type(search.json()["response"]["messages"][x][
                                        "id"]) == int, "Айди сообщения приходит в неккоретном формате"
                        x += 1
                    except IndexError:
                        assert x >= 5, "Возвращается больше 5 сообщений при запросе ALL"
                        x += 1
                while x < 50:
                    try:
                        assert type(search.json()["response"]["files"][x][
                                        "id"]) == int, "Айди файла приходит в неккоректном формате"
                        x += 1
                    except IndexError:
                        assert x >= 5, "Возвращается больше 5 файлов при запросе ALL"
                        x += 1
                while x < 50:
                    try:
                        assert type(search.json()["response"]["threads"][x][
                                        "id"]) == int, "Айди треда приходит в неккоректном формате"
                        x += 1
                    except IndexError:
                        assert x >= 5, "Возвращается больше 5 аредов при запросе ALL"
                        x += 1
            else:
                pytest.fail(
                    f"На данный тип поиска ({search_type}) нет проверки либо такого типа поиска не существует. Выберите один из этих типов поиска: ALL, THREAD, CONTACT, MESSAGE, FILE")


        elif status_code == 401:
            #Проверка 401 ошибки при отсутствии токена авторизации в запросе
            search = requests.get(self.search_request(search_chat=False),
                                  headers=None,
                                  json=self.search_json(s=s, offset=offset, limit=limit, search_type=search_type))
            assert search.status_code == 401, "Не возвращается 401 ответ при выполнении запрос без авторизации"
            assert search.json()["errMsg"] == self.no_auth_error, "Не возвращается ошибка в ответе при выполнении запроса без авторизации"
        elif status_code == 404:
            #Проверка выдачи ошибки при отсутствии строки в запросе(нет JSON'а)
            search = requests.get(self.search_request(search_chat=False),
                                  headers=self.get_headers(self.main_user_token_url))
            assert search.status_code == 200
            assert search.json()["errMsg"] == "s is null"
            #Проверка выдачи пустого ответа при отсутствии type в запросе
            json = {
                "s": "Hello"
            }
            search = requests.get(self.search_request(search_chat=False),
                                  headers=self.get_headers(self.main_user_token_url), json=json)
            assert search.status_code == 200
            assert search.json()["response"]["messages"] == [], "При отсутствии type в запросе должен выдаваться пустой ответ"
            assert search.json()["response"][
                       "files"] == [], "При отсутствии type в запросе должен выдаваться пустой ответ"
            assert search.json()["response"][
                       "contacts"] == [], "При отсутствии type в запросе должен выдаваться пустой ответ"
            assert search.json()["response"][
                       "threads"] == [], "При отсутствии type в запросе должен выдаваться пустой ответ"
            assert search.json()["response"][
                       "messages_other"] == [], "При отсутствии type в запросе должен выдаваться пустой ответ"
        else:
            pytest.fail(f"На данный статус кода ({status_code}) нет проверки. Выберите один из этих статусов кода: 200, 401, 404")

    def search_in_chat(self, chat_hash: str, s: str, offset: int, limit: int, status_code: int = 200):
        if status_code == 200:
            search_in_chat = requests.get(self.search_request(search_chat=True, chat_hash=chat_hash), headers=self.get_headers(self.main_user_token_url),
                                          json=self.search_in_chat_json(chat_hash=chat_hash, s=s, offset=offset, limit=limit))
            assert search_in_chat.status_code == 200
            x = 0
            while x < limit + 1:
                try:
                    search_in_chat_response = search_in_chat.json()["response"]["messages"]
                    assert type(search_in_chat_response[x][
                                    "id"]) == int, "ID сообщения возвращается в неккоректном формате в ответе"
                    assert type(search_in_chat_response[x]["hash"]) == str, "Хэш сообщения возвращается в неккоректном формате"
                    assert len(search_in_chat_response[x]["hash"]) == self.hash_length, "Хэш должен быть длиной в 36 символов"
                    assert type(search_in_chat_response[x]["created_at"]) == int, "Created at возвращается в неккоректном формате"
                    assert type(
                        search_in_chat_response[x]["user_hash"]) == str, "Хэш юзера возвращается в неккоректном формате"
                    assert len(search_in_chat_response[x][
                               "user_hash"]) == self.hash_length, "Хэш должен быть длиной в 36 символов"
                    assert type(
                        search_in_chat_response[x]["subject_hash"]) == str, "Хэш чата возвращается в неккоректном формате"
                    assert len(search_in_chat_response[x][
                               "hash"]) == self.hash_length, "Хэш должен быть длиной в 36 символов"
                    assert search_in_chat_response[x]["subject_hash"] == chat_hash, "Возвращается некорректный хэш чата в ответе"
                    assert type(search_in_chat_response[x]["subject_title"]) == str, "Subject Title возвращается в неккоректном формате"
                    if chat_hash == self.test_chat_hash:
                        assert search_in_chat_response[x]["subject_type"] == "private", "Возвращается некорректный тип чата в ответе"
                    x += 1
                except IndexError:
                    assert x <= limit, "Выдало больше сообщений, чем limit"
                    break
                except KeyError:
                    # Если Limit > 50, проверяем ошибку
                    if limit > 50:
                        assert search_in_chat.json()["errMsg"] == "limit, max 50", "Запрос работает при limit > 50"
                    break
        elif status_code == 401:
            #Проверка 401 ошибки при отсутствии токена авторизации в запросе
            search_in_chat = requests.get(self.search_request(search_chat=True, chat_hash=chat_hash),
                                          json=self.search_in_chat_json(chat_hash=chat_hash, s=s, offset=offset,
                                                                        limit=limit))
            assert search_in_chat.status_code == 401, "Не возвращается 401 ответ при выполнении запроса без авторизации"
            assert search_in_chat.json()[
                       "errMsg"] == self.no_auth_error, "Не возвращается ошибка в ответе при выполнении запроса без авторизации"
        elif status_code == 404:
            # Проверка выдачи ошибки при отсутствии строки в запросе(нет JSON'а)
            search_in_chat = requests.get(self.search_request(search_chat=True, chat_hash=chat_hash),
                                          headers=self.get_headers(self.main_user_token_url))
            assert search_in_chat.status_code == 200
            assert search_in_chat.json()["errMsg"] == "s is null"
            # Проверка выдачи пустого ответа при отсутствии hash в запросе
            json = {
                "s": "Hello"
            }
            search_in_chat = requests.get(self.search_request(search_chat=True),
                                          headers=self.get_headers(self.main_user_token_url), json=json)
            assert search_in_chat.status_code == 404, "Не возвращается 404 ответ при выполнении запроса без хэша чата"
            assert search_in_chat.json()["errMsg"] == "Not found method", "Не возвращается ошибка при выполнении запроса без хэша чата"
        else:
            pytest.fail(f"На данный статус кода ({status_code}) нет проверки. Выберите один из этих статусов кода: 200, 401, 404")




    def global_search(self):
        self.search(status_code=401, s="Test", offset=0, limit=1000, search_type="THREAD")
        self.search(status_code=404, s="Test", offset=0, limit=1000, search_type="THREAD")
        self.search(status_code=200, s="Привет", limit=50, offset=50, search_type="MESSAGE")
        self.search(status_code=200, s="Hello", limit=25, offset=50, search_type="MESSAGE")
        self.search(status_code=200, s="TEST", limit=100, offset=50, search_type="MESSAGE")
        self.search(status_code=200, s="Test", offset=0, limit=60, search_type="FILE")
        self.search(status_code=200, s="Test", offset=0, limit=25, search_type="FILE")
        self.search(status_code=200, s="Testik Testov", offset=0, limit=2, search_type="CONTACT")
        self.search(status_code=200, s="Testik Testov", offset=0, limit=51, search_type="CONTACT")
        self.search(status_code=200, s="тред", offset=0, limit=15, search_type="THREAD")
        self.search(status_code=200, s="тред", offset=0, limit=55, search_type="THREAD")
        self.search(status_code=200, s="тред", offset=0, limit=25, search_type="THREAD")
        self.search(status_code=200, s="Test", offset=0, limit=15, search_type="ALL")

    def full_search_in_chat(self):
        self.search_in_chat(status_code=404, chat_hash=self.test_chat_hash, s="Test", offset=30, limit=1000)
        self.search_in_chat(status_code=401, chat_hash=self.test_chat_hash, s="Test", offset=30, limit=1000)
        self.search_in_chat(chat_hash=self.test_chat_hash, s="Test", offset=30, limit=1)
        self.search_in_chat(chat_hash=self.test_chat_hash, s="Test", offset=30, limit=1000)

