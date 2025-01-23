import json
from typing import Optional
import requests
from Chat.ChatJson import ChatJson


class Chat(ChatJson):
    def __init__(self):
        super().__init__()
        self.title_null_error = "title is null"
        self.roles_array = ["ADMIN", "OWNER"]

    def get_chat_information(self,
                             chat_hash: Optional[str] = None,
                             headers: Optional[dict] = None,
                             status_code: Optional[int] = None):
        if status_code == 200:
            req = requests.get(f"{self.main_api_url}/chat/{chat_hash}", json=self.json_for_get_chat_info(chat_hash),
                               headers=headers)
            expected_keys = {"hash", "title", "translate_key", "description", "avatar", "avatars", "type", "created_at", "created_by",
                             "updated_at", "hidden_at", "notification", "is_draft", "users"}
            # print(json.dumps(req.json(), indent=4))
            assert req.status_code == 200, "Запрос на информацию о чате не работает"
            # Проверка типа отдаваемых данных
            assert isinstance(req.json()["response"]["hash"], str)
            assert isinstance(req.json()["response"]["title"], str)
            assert isinstance(req.json()["response"]["hash"], str)
            assert isinstance(req.json()["response"]["hash"], str)
            # print(json.dumps(req.json()["response"]["folders"], indent=4))
            req.raise_for_status()
            return [req.json()["response"]["folders"], req.json()]

    def get_popular_chats(self,
                          status_code: Optional[int] = None,
                          headers: Optional[dict] = None):
        if status_code == 200:
            req = requests.get(f"{self.main_api_url}/chat/popular", json=self.base_json(), headers=headers)
            # Проверяем, что значения sort идут от большего к меньшему
            sort_values = [item["sort"] for item in req.json()["response"]["items"]]
            is_sorted_descending = all(sort_values[i] >= sort_values[i + 1] for i in range(len(sort_values) - 1))
            assert is_sorted_descending == True, "параметр sort должен выдаваться от меньшего к большему"
            response_items = req.json()["response"]["items"]
            assert len(response_items) <= 10, "Должно возвращаться не больше 10 популярных чатов"
            # Создание множеств для ключей hash и sort
            hash_set = set(item["hash"] for item in response_items)
            sort_set = set(item["sort"] for item in response_items)
            # Проверка, что длина множества совпадает с длиной исходного списка
            hash_unique = len(hash_set) == len(response_items)
            sort_unique = len(sort_set) == len(response_items)
            print(hash_unique, sort_unique)
            assert hash_unique == True, "Hash чата должен быть уникальным"
            try:
                assert sort_unique == True, "Sort чата должен быть уникальным"
            except AssertionError:
                self.send_info_in_debug_bot("Sort параметры популярных чатов не одинаковы")
        elif status_code == 401:
            req = requests.get(f"{self.main_api_url}/chat/popular", json=self.base_json(), headers=None)
            assert req.status_code == 401, "Не выдается ошибка при выполнении запроса без авторизации"
            assert req.json()["errMsg"] == self.no_auth_error, "Не выдается ошибка при выполнении запроса без авторизации"
        elif status_code is None:
            # Некорректные заголовки авторизации
            headers = {"token": self.generate_random_string(15), "hash": self.generate_random_string(20)}
            req = requests.get(f"{self.main_api_url}/chat/popular", json=self.base_json(), headers=headers)
            assert req.status_code == 401, "Не выдается ошибка при выполнении запроса без авторизации"
            assert req.json()["errMsg"] == self.no_auth_error2, "Не выдается ошибка при выполнении запроса без авторизации"

    def get_chat_list_count(self,
                            status_code: Optional[int] = None,
                            headers: Optional[dict] = None,
                            is_archive: Optional[bool] = None):
        if status_code == 200:
            req = requests.get(f"{self.main_api_url}/chat/list/count", headers=headers,
                               json=self.json_for_get_chat_list_count(is_archive=is_archive))
            assert req.status_code == 200, "Запрос не работает"
            if is_archive is True:
                assert req.json()["response"]["count"] <= 500, "Запрос возвращает некорректное кол-во архивных чатов"
            elif is_archive is False:
                assert req.json()["response"]["count"] >= 2000, "Запрос возвращает некорректное кол-во не архивных чатов"
            elif is_archive is None:
                assert req.json()["response"][
                           "count"] >= 2000, "Запрос без указания is_archive всегда должен возвращать кол-во не архивных чатов"
        if status_code == 401:
            req = requests.get(f"{self.main_api_url}/chat/list/count", headers=None,
                               json=self.json_for_get_chat_list_count(is_archive=is_archive))
            assert req.status_code == 401, "Не выдается ошибка при выполнении запроса без авторизации"
            assert req.json()[
                       "errMsg"] == self.no_auth_error, "Не выдается ошибка при выполнении запроса без авторизации"


    # Получение кол-во доступных каналов для пользователя
    def get_available_channel_list_count(self,
                                         status_code: Optional[int] = 200,
                                         headers: Optional[dict] = None):
        if status_code == 200:
            req = requests.get(f"{self.main_api_url}/chat/channel/list/count", headers=headers, json=self.base_json())
            assert req.status_code == 200, "Запрос не работает"
            assert req.json()["response"]["count"] >= 100, "Сервер возвращает некорректное кол-во каналов"
        elif status_code == 401:
            req = requests.get(f"{self.main_api_url}/chat/channel/list/count", headers=None, json=self.base_json())
            assert req.status_code == 401, "Не выдается ошибка при выполнении запроса без авторизации"
            assert req.json()[
                       "errMsg"] == self.no_auth_error, "Не выдается ошибка при выполнении запроса без авторизации"

    def get_chats_allow_for_invite(self,
                                   status_code: Optional[int] = 200,
                                   headers: Optional[dict] = None):
        if status_code == 200:
            add_user_array = [True, False]
            req = requests.get(f"{self.main_api_url}/chat/allow_invite", headers=headers, json=self.base_json())
            response_data = req.json()["response"]
            for data in response_data:
                assert data["add"] in add_user_array, "параметр add возвращается некорректно"
                if data["add"] is False:
                    chat_data = self.get_chat_information(chat_hash=data["hash"], headers=headers, status_code=status_code)[1]
                    users_list = self.get_users_from_chat(status_code=200, headers=headers, chat_hash=data["hash"])[0]["response"]
                    for user_data in users_list:
                        user_hash = user_data["hash"]
                        request_data = self.get_user_profile(user_hash=user_hash, status_code=200, headers=headers)[1]["response"]
                        # print(request_data)
                        if request_data["name"] == self.main_user_name and request_data["surname"] == self.main_user_surname:
                            try:
                                assert request_data["role"] in self.roles_array, ("Юзеру не должен выдаваться чат, "
                                                                                  "если у него нет права приглашения другого участника в него")
                            except AssertionError:
                                assert chat_data["response"]["settings"]["user_add_user"] is True, ("Юзеру не должен выдаваться чат, "
                                                                                                    "если у него нет права приглашения другого участника в него")

            # Извлечение всех хешей в отдельный список
            hash_list = [h['hash'] for h in response_data]
            unique_hashes = set(hash_list)
            assert len(unique_hashes) == len(hash_list), "Возвращаемые хэши чатов должны быть уникальны и не должны повторяться"

        elif status_code == 401:
            req = requests.get(f"{self.main_api_url}/chat/allow_invite", headers=None, json=self.base_json())
            assert req.status_code == 401, "Не выдается ошибка при выполнении запроса без авторизации"
            assert req.json()[
                       "errMsg"] == self.no_auth_error, "Не выдается ошибка при выполнении запроса без авторизации"

    def rename_chat(self,
                    status_code: Optional[int] = 200,
                    headers: Optional[dict] = None,
                    new_title: Optional[str] = None,
                    chat_hash: Optional[str] = None,
                    available_hash: Optional[bool] = None):
        if available_hash is True and chat_hash is None:
            chat_hash = "3929e197-6106-41ea-b9e8-94f92f82f672"
        elif available_hash is False and chat_hash is None:
            chat_hash = "141f6379-9ba4-4462-b37e-1803680b7c20"
        elif available_hash is None and chat_hash is None:
            chat_hash = chat_hash
        if status_code == 200:
            req = requests.put(f"{self.main_api_url}/chat/{chat_hash}/title",
                               json=self.json_for_rename_chat_name(hash_chat=chat_hash, title=new_title),
                               headers=headers)
            if available_hash is True:
                assert req.status_code == 200, "Запрос на смену название чата не работает"
                assert req.json()["response"] is True, "Смена названия в чате не работает"
                chat_data = self.get_chat_information(chat_hash=chat_hash, status_code=200, headers=headers)[1]
                assert chat_data["response"]["title"] == new_title, "Не работает переименование чата"
            elif available_hash is False:
                assert req.status_code == 200, "Запрос на смену название чата не работает" # Даже при ошибке бэк возвращает 200-ый статус
                assert req.json()["errMsg"] == self.not_access_error, "В ответе отсутствует ошибка при попытке редактирования чата без прав доступа"#
        elif status_code == 401:
            req = requests.put(f"{self.main_api_url}/chat/{chat_hash}/title",
                               json=self.json_for_rename_chat_name(hash_chat=chat_hash, title=new_title),
                               headers=None)
            assert req.status_code == 401, "Не выдается ошибка при выполнении запроса без авторизации"
            assert req.json()[
                       "errMsg"] == self.no_auth_error, "Не выдается ошибка при выполнении запроса без авторизации"
        elif status_code == 404:
            if available_hash is None and chat_hash is None:
                chat_hash = chat_hash
                req = requests.put(f"{self.main_api_url}/chat/{chat_hash}/title",
                                   json=self.json_for_rename_chat_name(hash_chat=chat_hash, title=new_title),
                                   headers=headers)
                assert req.status_code == 404, "Не возвращается ошибка при выполнении запроса без хэша чата"
                assert req.json()["errMsg"] == self.not_found_methods_error, "Не возвращается ошибка при выполнении запроса без хэша чата"
            elif available_hash is True or False and new_title is None:
                chat_hash = "3929e197-6106-41ea-b9e8-94f92f82f672"
                req = requests.put(f"{self.main_api_url}/chat/{chat_hash}/title",
                                   json=self.json_for_rename_chat_name(hash_chat=chat_hash, title=new_title),
                                   headers=headers)
                assert req.json()["errMsg"] == self.title_null_error, "Не возвращается ошибка при выполнении запроса без title чата"
                # Даже при ошибке бэк возвращает 200-ый статус
                assert req.status_code == 200, "Запрос на смену название чата не работает"


















