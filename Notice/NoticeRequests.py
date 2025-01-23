import pytest
import requests
from Auth.AuthJson import json_for_api_version
from Notice.Json import NoticeJson


class Notice(NoticeJson):
    def __init__(self):
        super().__init__()
        self.notice_status_array = ["CANCELED", "FINISHED", "ACTIVE"]
        self.import_param_array = [True, False]

    def get_notice(self, status_code: int = 200, only_return_notice_id: bool = False):
        if status_code == 200:
            get_notice_request = requests.get(f"{self.main_api_url}/notice", headers=self.get_headers(self.main_user_token_url), json=json_for_api_version)
            assert get_notice_request.status_code == 200, "Не прошел запрос на получение оповещений"
            if only_return_notice_id == False:
                x = 0
                while x < 50:
                    try:
                        notice_response = get_notice_request.json()["response"][x]
                        assert type(notice_response["id"]) == str, "Айди оповещения возвращается в неккоректном формате"
                        assert len(notice_response["id"]) == self.hash_length, "Хэш должен быть длиной в 36 символов"
                        assert type(
                            notice_response["created_at"]) == int, "Created_at возвращается в неккоректном формате"
                        assert type(
                            notice_response["updated_at"]) == int, "Updated_at возвращается в неккоректном формате"
                        assert type(notice_response["date"]) == int, "Date возвращается в неккоректном формате"
                        assert type(
                            notice_response["description"]) == str, "Description возвращается в неккоректном формате"
                        assert notice_response["status"] in self.notice_status_array, "Не возвращается статус оповещения"
                        assert notice_response["is_important"] in self.import_param_array, "Параметр is_important должен возвращаться в формате bool"
                        x += 1
                    except IndexError:
                        break
            elif only_return_notice_id == True:
                return get_notice_request.json()["response"][0]["id"]
        elif status_code == 401:
            get_notice_request = requests.get(f"{self.main_api_url}/notice",
                                              json=json_for_api_version)
            assert get_notice_request.status_code == 401, "Не возвращается 401 ответ при выполнении запроса без авторизации"
            assert get_notice_request.json()["errMsg"] == self.no_auth_error, "Не возвращается ошибка при выполнении запроса без авторизации"
        else:
            pytest.fail(f"На данный статус ответа ({status_code}) отсутствует проверка. Попробуйте статусы ответа: 200, 401")
    def get_one_notice(self, notice_id: str ,status_code: int = 200):
        if status_code == 200:
            get_one_notice_request = requests.get(f"{self.main_api_url}/notice/{self.test_chat_hash}", headers = self.get_headers(self.main_user_token_url), json=self.json_for_one_notice(
                notice_id))
            assert get_one_notice_request.status_code == 200, "Запрос на получение одного оповещения не работает"
            one_notice_response = get_one_notice_request.json()["response"]
            assert type(one_notice_response["id"]) == str, "Айди оповещения возвращается в неккоректном формате"
            assert one_notice_response["id"] == notice_id, "Возвращается не то айди оповещения по которому идет запрос"
            assert type(one_notice_response["created_at"]) == int, "Параметр created_at возвращается в неккоректном формате"
            assert type(one_notice_response["updated_at"]) == int, "Параметр updated_at возвращается в неккоректном формате"
            assert type(one_notice_response["date"]) == int, "Параметр date возвращается в неккоректном формате"
            assert type(one_notice_response["description"]) == str, "Параметр description возвращается в неккоректном формате"
            assert type(one_notice_response["updated_at"]), "Параметр updated_at возвращается в неккоректном формате"
            assert one_notice_response["status"] in self.notice_status_array, "Не возвращается статус оповещения"
            assert type(one_notice_response["is_important"]) == bool, "Параметр is_important должен возвращаться в формате bool"
            assert one_notice_response["is_important"] in self.import_param_array, "Параметр is_important должен возвращаться в формате bool"
        elif status_code == 401:
            get_one_notice_request = requests.get(f"{self.main_api_url}/notice/{self.test_chat_hash}",
                                                  json=self.json_for_one_notice(notice_id))
            assert get_one_notice_request.status_code == 401, "Не возвращается 401 статус кода при выполнении запроса без авторизации"
            assert get_one_notice_request.json()["errMsg"] == self.no_auth_error, "Не возвращается статус кода при выполнении запроса без авторизации"
        elif status_code == 404:
            get_one_notice_request = requests.get(f"{self.main_api_url}/notice/{self.test_chat_hash}",
                                                  headers=self.get_headers(self.main_user_token_url))
            assert get_one_notice_request.json()["errMsg"] == "id not found", "Не возвращается ошибка при отсутствии айди оповещения в запросе"
            get_one_notice_request = requests.get(f"{self.main_api_url}/notice/3ifhi3hf",
                                                  headers=self.get_headers(self.main_user_token_url), json=self.json_for_one_notice(
                    notice_id))
            assert get_one_notice_request.status_code == 404, "Не возвращается 404 статус кода при отсутствии хэша чата в запросе"
            assert get_one_notice_request.json()["errMsg"] == self.not_found_methods_error, "Не возвращается ошибка при отсутствии хэша чата в запросе"
        else:
            pytest.fail(
                f"На данный статус ответа ({status_code}) отсутствует проверка. Попробуйте статусы ответа: 200, 401, 404")

    def add_notice(self, description: str, date: int, is_important: bool, subject_hash: str, status_code: int = 200):
        if status_code == 200:
            add_notice_request = requests.post(f"{self.main_api_url}/notice", headers=self.get_headers(self.main_user_token_url),
                                               json=self.json_for_add_notice(description=description, timestamp=date, is_important=is_important, subject_hash=subject_hash))
            assert add_notice_request.status_code == 200, "Не работает запрос"
            add_notice_response = add_notice_request.json()["response"]
            assert type(add_notice_response["id"]) == str, "Айди оповещения возвращается в некорректном формате"
            assert type(add_notice_response["is_important"]) == bool, "Параметр is_important возвращается в некорректном формате"
            assert add_notice_response["is_important"] == is_important, "Параметр is_important возвращается некорректно"
            return [add_notice_response["id"], date]
        elif status_code == 401:
            add_notice_request = requests.post(f"{self.main_api_url}/notice",
                                               json=self.json_for_add_notice(description=description, timestamp=date,
                                                                             is_important=is_important,
                                                                             subject_hash=subject_hash))
            assert add_notice_request.status_code == 401, "Не возвращается 401 статус кода при выполнении запроса без авторизации"
            assert add_notice_request.json()["errMsg"] == self.no_auth_error, "Не возвращается ошибка кода при выполнении запроса без авторизации"
        elif status_code == 404:
            #Date is empty
            add_notice_request = requests.post(f"{self.main_api_url}/notice",
                                               headers=self.get_headers(self.main_user_token_url))
            assert add_notice_request.json()["errMsg"] == "date not found", "Не возвращается ошибка при пустой date в запросе"
            #Description is empty
            add_notice_request = requests.post(f"{self.main_api_url}/notice",
                                               headers=self.get_headers(self.main_user_token_url),
                                               json=self.json_for_add_notice(description=None, timestamp=date,
                                                                             is_important=is_important,
                                                                             subject_hash=subject_hash))
            assert add_notice_request.json()[
                       "errMsg"] == "description not found", "Не возвращается ошибка при пустом description в запросе"
            #Subject_hash is empty
            add_notice_request = requests.post(f"{self.main_api_url}/notice",
                                               headers=self.get_headers(self.main_user_token_url),
                                               json=self.json_for_add_notice(description="ТЕСТ", timestamp=date,
                                                                             is_important=is_important,
                                                                             subject_hash=None))
            assert add_notice_request.status_code == 200, "Запрос с пустым subject_hash не работает"
            assert type(add_notice_request.json()["response"]["id"]) == str, "Айди оповещения возвращается в некорректном формате"
            assert type(add_notice_request.json()["response"]["is_important"]) == bool, "Параметр is_important возвращается в некорректном формате"
            assert add_notice_request.json()["response"]["is_important"] == is_important, "Параметр is_important возвращается некорректно"




    def add_notice_requests(self):
        notice_data = self.add_notice(status_code=200, description="Test", date=self.current_data.isoformat(), is_important=True, subject_hash=self.test_chat_hash)
        self.add_notice(status_code=401, description="Test", date=self.current_data.isoformat(), is_important=True, subject_hash=self.test_chat_hash)
        self.add_notice(status_code=404, description="Test", date=self.current_data.isoformat(), is_important=True, subject_hash=self.test_chat_hash)
        return notice_data

    def edit_notice(self, notice_id: (str, None), description: (None, str), date, status_code: int = 200):
        if status_code == 200:
            edit_notice_request = requests.put(f"{self.main_api_url}/notice/{self.test_chat_hash}", headers=self.get_headers(self.main_user_token_url), json=self.json_for_edit_notice(notice_id=notice_id, description=description, date=date))
            print(edit_notice_request.json())
            assert edit_notice_request.status_code == 200, "Запрос на редактирование оповещения не работает"
            assert edit_notice_request.json()["response"] == True, "Запрос на редактирование оповещения не работает"
        elif status_code == 401:
            edit_notice_request = requests.put(f"{self.main_api_url}/notice/{self.test_chat_hash}",
                                               json=self.json_for_edit_notice(notice_id=notice_id,
                                                                              description=description, date=date))
            assert edit_notice_request.status_code == 401, "Не возвращается 401 статус кода при выполнении запроса без авторизации"
            assert edit_notice_request.json()["errMsg"] == self.no_auth_error, "Не возвращается ошибка кода при выполнении запроса без авторизации"
        elif status_code == 404:
            #id is empty
            edit_notice_request = requests.put(f"{self.main_api_url}/notice/{self.test_chat_hash}",
                                               headers=self.get_headers(self.main_user_token_url))
            assert edit_notice_request.json()["errMsg"] == "id not found", "Не возвращается ошибка, если делать запрос без айди оповещения"
            #Description is empty
            edit_notice_request = requests.put(f"{self.main_api_url}/notice/{self.test_chat_hash}",
                                               headers=self.get_headers(self.main_user_token_url),
                                               json=self.json_for_edit_notice(notice_id=notice_id,
                                                                              description=None, date=date))
            assert edit_notice_request.json()["response"] == True, "Возвращается ошибка при редактировании с пустым описанием оповещением"
            #Date is empty
            edit_notice_request = requests.put(f"{self.main_api_url}/notice/{self.test_chat_hash}",
                                               headers=self.get_headers(self.main_user_token_url),
                                               json=self.json_for_edit_notice(notice_id=notice_id,
                                                                              description=description, date=None))
            assert edit_notice_request.json()[
                       "response"] == True, "Возвращается ошибка при редактировании с пустой временной меткой"






    def delete_notice(self, notice_id: str ,status_code: int = 200):
        if status_code == 200:
            delete_notice_request = requests.delete(f"{self.main_api_url}/notice/{self.test_chat_hash}", headers=self.get_headers(self.main_user_token_url), json=self.json_for_one_notice(notice_id))
            assert delete_notice_request.status_code == 200, "Запрос на удаление оповещения не работает"
            assert delete_notice_request.json()["response"] == True, "Запрос на удаление оповещения не работает"
        elif status_code == 401:
            delete_notice_request = requests.delete(f"{self.main_api_url}/notice/{self.test_chat_hash}",
                                                    json=self.json_for_one_notice(notice_id))
            assert delete_notice_request.status_code == 401, "Не возвращается 401 статус ответа после выполнения запроса без авторизации"
            assert delete_notice_request.json()["errMsg"] == self.no_auth_error, "Не возвращается ошибка после выполнения запроса без авторизации"
        elif status_code == 404:
            delete_notice_request = requests.delete(f"{self.main_api_url}/notice/{self.test_chat_hash}",
                                                    headers=self.get_headers(self.main_user_token_url))
            assert delete_notice_request.json()["errMsg"] == "id not found", "Не возвращается ошибка после выполнения запроса без айди оповещения"

    def finish_notice(self, notice_id: str ,status_code: int = 200):
        if status_code == 200:
            finish_notice_request = requests.put(f"{self.main_api_url}/notice/{self.test_chat_hash}/finish", headers=self.get_headers(self.main_user_token_url), json=self.json_for_one_notice(notice_id))
            assert finish_notice_request.status_code == 200, "Не работает запрос на завершение оповещения"
            assert finish_notice_request.json()["response"] == True, "Не работает запрос на завершение оповещения"
        elif status_code == 401:
            finish_notice_request = requests.put(f"{self.main_api_url}/notice/{self.test_chat_hash}/finish",
                                                 json=self.json_for_one_notice(notice_id))
            assert finish_notice_request.status_code == 401, "Не возвращается 401 статус ответа после выполнения запроса без авторизации"
            assert finish_notice_request.json()["errMsg"] == self.no_auth_error, "Не возвращается ошибка после выполнения запроса без авторизации"
        elif status_code == 404:
            finish_notice_request = requests.put(f"{self.main_api_url}/notice/{self.test_chat_hash}/finish",
                                                 headers=self.get_headers(self.main_user_token_url))
            assert finish_notice_request.json()["errMsg"] == "id not found", "Не возвращается ошибка после выполнения запроса без айди оповещения"








