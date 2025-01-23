import json
from typing import Optional, Union

import pytest
import requests
from Folder.FolderJson import FolderJson
from Section.SectionRequests import chat_hash


class Folder(FolderJson):

    folder_hash_array = []  # Массив для хранения хэшей папок в массиве
    folder_titles_array = [] # Массив для хранения названий папок в массиве

    def __init__(self):
        super().__init__()
        self.not_found_title_error = "not found title"
        self.not_found_subject_hash_error = "not found subject_hash"
        self.hash_dict = {}
        self.previous_sort = None # Инициализация предыдущего значения параметра sort
        self.folder_hash = None, # Атрибут для хранения хэша созданной папки

    def create_folder_in_chat(
            self,
            subject_hash: Optional[str] = None,
            sort: Optional[int] = None,
            title: Optional[Union[str, int, float]] = None,
            headers: Optional[dict] = None,
            status_code: Optional[int] = None,
            empty_title: Optional[bool] = False,
            empty_subject_hash: Optional[bool] = False,
            empty_sort_param: Optional[bool] = False
    ):
        if status_code == 200:
            response = requests.post(f"{self.main_api_url}/folder", json=self.json_for_create_folder(subject_hash=subject_hash,
                                                                                                     title=title,
                                                                                                     sort=sort),
                                     headers=headers)
            assert response.status_code == 200, "Запрос не работает"
            assert abs(self.current_unix_timestamp - response.json()["response"]["created_at"]) <= 20, \
                "Created_at возвращает некорректную временную метку"
            assert len(response.json()["response"]["hash"]) == 36
            assert type(response.json()["response"]["hash"]) == str
            assert response.json()["response"]["title"] == title, "Возвращается некорректное название созданной папки"
            assert float(response.json()["response"]["sort"]) == sort, "Возвращается некорректный параметр сортировки папки"
            assert response.json()["response"]["is_empty"] == True
            # Сохранение полученного хэша папки
            folder_hash = response.json()["response"]["hash"]
            Folder.folder_hash_array.append(folder_hash)
            # Сохранение полученного title папки
            folder_title = response.json()["response"]["title"]
            Folder.folder_titles_array.append(folder_title)

        if status_code == 401:
            response = requests.post(f"{self.main_api_url}/folder",
                                     json=self.json_for_create_folder(subject_hash=subject_hash,
                                                                      title=title,
                                                                      sort=sort)
                                     )
            assert response.status_code == 401, "Не возвращается 401, если пользователь делает запрос без авторизации"
            assert response.json()["errMsg"] == self.no_auth_error, "Не возвращается ошибка, если пользователь делает запрос без авторизации"
        elif status_code is None:

            if empty_title is True:
                # Запрос без параметра title
                response = requests.post(f"{self.main_api_url}/folder",
                                         json=self.json_for_create_folder(subject_hash=subject_hash,
                                                                          title=None,
                                                                          sort=sort),
                                         headers=headers)
                assert response.json()["errMsg"] == self.not_found_title_error
            elif empty_subject_hash is True:
                response = requests.post(f"{self.main_api_url}/folder",
                                         json=self.json_for_create_folder(subject_hash=None,
                                                                          title=title,
                                                                          sort=sort),
                                         headers=headers)
                assert response.json()["errMsg"] == self.not_found_subject_hash_error
            elif empty_sort_param is True:
                response = requests.post(f"{self.main_api_url}/folder",
                                         json=self.json_for_create_folder(subject_hash=subject_hash,
                                                                          title=title,
                                                                          sort=None),
                                         headers=headers)
                current_sort_param = float(response.json()["response"]["sort"])
                folder_hash = response.json()["response"]["hash"]
                Folder.folder_hash_array.append(folder_hash)
                if self.previous_sort is not None:
                    if current_sort_param - self.previous_sort != 1:
                        print(f"Ошибка: sort увеличился не на 1. "
                              f"Предыдущее значение: {self.previous_sort}, текущее: {current_sort_param}")
                    else:
                        print(f"Параметр sort корректно увеличился на 1. Текущее значение: {current_sort_param}")
                else:
                    print(f"Первое выполнение. Текущее значение sort: {current_sort_param}")

                    # Обновляем предыдущее значение sort
                self.previous_sort = current_sort_param
                return response.json()

    def delete_folder(self, folder_hash: Optional[str] = None,
                      status_code: Optional[int] = None,
                      headers: Optional[dict] = None,
                      non_existent_hash: Optional[bool] = False,
                      hash_chat: Optional[str] = None):
        if status_code == 200:
            if folder_hash is None:
                if not Folder.folder_hash_array:
                    self.send_info_in_debug_bot(message="Массив хэшей папок пуст")
                folder_hash = Folder.folder_hash_array.pop(0)
            request = requests.delete(f"{self.main_api_url}/folder/{folder_hash}",
                                      headers=headers)
            assert request.status_code == 200, "Выполнение запроса не работает"
            assert request.json()["response"] == True, "Запрос на удаление папки не работает"
            folders_data = self.get_chat_information(chat_hash=hash_chat, headers=headers, status_code=200)
            found = any(item['hash'] == folder_hash for sublist in folders_data for item in sublist)
            assert found == False, "Удаление папки из чата не работает"

        if status_code == 401:
            request = requests.delete(f"{self.main_api_url}/folder/{folder_hash}", headers=None)
            assert request.status_code == 401, "Не возвращается 401, если пользователь делает запрос без авторизации"
            assert request.json()[
                       "errMsg"] == self.no_auth_error, "Не возвращается ошибка, если пользователь делает запрос без авторизации"

        if status_code is None and non_existent_hash is True:
                if folder_hash is None:
                    folder_hash = self.generate_random_string(36)
                request = requests.delete(f"{self.main_api_url}/folder/{folder_hash}", headers=headers)
                assert request.status_code == 404, "Не возвращается статус 404, когда юзер пытается удалить несуществующую папку"

    def folder_sort(self, folder_hash: Optional[str] = None,
                    sort: Optional[int] = None,
                    status_code: Optional[int] = None,
                    headers: Optional[dict] = None,
                    empty_sort_param: Optional[bool] = False,
                    empty_folder_hash: Optional[bool] = False):
        if status_code == 200:
            if folder_hash is None:
                try:
                    folder_hash = Folder.folder_hash_array[0]
                except IndexError:
                    self.send_info_in_debug_bot("Массив пустой в тесте на сортировку папок")
            if sort is None:
                sort = self.generate_random_number(300, 1000)
            request = requests.put(f"{self.main_api_url}/folder/{folder_hash}/sort", json=self.json_for_sort_folder(sort=sort,
                                                                                                                    folder_hash=folder_hash),
                                   headers=headers)
            assert request.status_code == 200, "Выполнение запроса не работает"
            assert request.json()["response"] == True, "Выполнение запроса не работает"

        elif status_code == 401:
            if folder_hash is None:
                try:
                    folder_hash = Folder.folder_hash_array[0]
                except IndexError:
                    self.send_info_in_debug_bot("Массив пустой в тесте на сортировку папок")
            if sort is None:
                sort = self.generate_random_number(300, 1000)
            request = requests.put(f"{self.main_api_url}/folder/{folder_hash}/sort",
                                   json=self.json_for_sort_folder(sort=sort,
                                                                  folder_hash=folder_hash))
            assert request.status_code == 401, "Не возвращается 401, если пользователь делает запрос без авторизации"
            assert request.json()["errMsg"] == self.no_auth_error, "Не возвращается ошибка, если пользователь делает запрос без авторизации"
        elif status_code is None and empty_folder_hash is True:
            if folder_hash is None:
                folder_hash = self.generate_random_string(36)
            request = requests.put(f"{self.main_api_url}/folder/{folder_hash}/sort",
                                   json=self.json_for_sort_folder(sort=sort, folder_hash=folder_hash),
                                   headers=headers)
            assert request.status_code == 404, "Не возвращается 404 при выполнении запроса без указания хэша папки"
            assert request.json()["errMsg"] == self.not_found_methods_error, "Не возвращается ошибка при выполнении запроса без указания хэша папки"
        elif status_code is None and empty_sort_param is True:
            if folder_hash is None:
                folder_hash = Folder.folder_hash_array[0]
            sort = None
            request = requests.put(f"{self.main_api_url}/folder/{folder_hash}/sort",
                                   json=self.json_for_sort_folder(sort=sort, folder_hash=folder_hash),
                                   headers=headers)
            assert request.status_code == 200, "Запрос должен выполнять успешно без указания параметра сортировки"
            assert request.json()["response"] == True, "Запрос должен выполняться успешно без указания параметра сортировки"

    def rename_folder(self, title: Optional[str] = None,
                      folder_hash: Optional[str] = None,
                      status_code: Optional[int] = None,
                      headers: Optional[dict] = None,
                      empty_folder_hash: Optional[bool] = False,
                      empty_folder_title: Optional[bool] = False,
                      hash_chat: Optional[str] = None):
        if status_code == 200:
            if folder_hash is None:
                folder_hash = Folder.folder_hash_array[0]
            if title is None:
                title = self.generate_random_string(29)
            request = requests.put(f"{self.main_api_url}/folder/{folder_hash}/title",
                                   json=self.json_for_rename_folder_title(title=title, folder_hash=folder_hash),
                                   headers=headers)
            folders_data = self.get_chat_information(chat_hash=hash_chat, headers=headers, status_code=200)
            found = any(item['title'] == title for sublist in folders_data for item in sublist)
            assert found == True, "Изменение названия папки в чате не работает"
        elif status_code == 401:
            if folder_hash is None:
                folder_hash = Folder.folder_hash_array[0]
            if title is None:
                title = self.generate_random_string(29)
            request = requests.put(f"{self.main_api_url}/folder/{folder_hash}/title",
                                   json=self.json_for_rename_folder_title(title=title, folder_hash=folder_hash))
            assert request.status_code == 401, "Не возвращается ошибка, если запрос был выполнен без авторизации"
            assert request.json()["errMsg"] == self.no_auth_error, "Не возвращается ошибка, если запрос был выполнен без авторизации"
        if status_code is None and empty_folder_hash is True:
            if title is None:
                title = self.generate_random_string(29)
            request = requests.put(f"{self.main_api_url}/folder/{folder_hash}/title",
                                   json=self.json_for_rename_folder_title(title=title, folder_hash=folder_hash),
                                   headers=headers)
            assert request.status_code == 404, "Не возвращается ошибка при выполнении запроса без указания хэша папки"
            assert request.json()["errMsg"] == self.not_found_methods_error, "Не возвращается ошибка при выполнении запроса без указания хэша папки"
        if status_code is None and empty_folder_title is True:
            if folder_hash is None:
                folder_hash = Folder.folder_hash_array[0]
            request = requests.put(f"{self.main_api_url}/folder/{folder_hash}/title",
                                   json=self.json_for_rename_folder_title(title=title, folder_hash=folder_hash),
                                   headers=headers)
            assert request.json()[
                       "errMsg"] == self.not_found_title_error, "Не возвращается ошибка, если запрос выполняется без указания имени папки"






























