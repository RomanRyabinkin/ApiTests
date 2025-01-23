import json

import pytest
import requests
from Login.Email import GenerateEmail
from Login.GetIp import UserIp
from Login.Json import LoginJson


class Login(LoginJson, UserIp, GenerateEmail):
    def __init__(self):
        super().__init__()
        self.user_id = 15764
        self.main_company_domain = "hello_world123"
        self.main_user_login = "roman_ryabinkin111"
        self.main_user_name = "Roman"
        self.main_user_surname = "Ryabinkin"
        self.main_user_email = "r0main.ryabinkin@yandex.ru"
        self.main_user_role = "OWNER"
        self.main_user_city = "New"
        self.main_user_timezone = "Europe/Moscow"
        self.main_company_id = 4170
        self.bool_array = [True, False]
        self.main_user_status = "ACTIVE"
        self.user_status_array = ["CANCELED", "FINISHED", "ACTIVE", "INVITED"]

    def get_login(self, status_code: int = 200):
        if status_code == 200:
            get_token_request = requests.get(f"{self.main_api_url}/login",
                                             headers=self.get_headers(self.main_user_token_url), json=self.base_json())
            assert get_token_request.status_code == 200, "Не работает запрос"
            get_token_response = get_token_request.json()["response"]
            assert get_token_response["user_id"] == self.user_id, "Возвращается неккоректный юзер айди"
            assert type(get_token_response[
                            "count_unread_message"]) == int, "count_unread_message возвращается в неккоректном формате"
            assert type(get_token_response[
                            "count_unread_subject"]) == int, "count_unread_subject возвращается в неккоректном формате"
            assert type(get_token_response[
                            "count_unread_thread"]) == int, "count_unread_thread возвращается в неккоректном формате"
            assert type(get_token_response["profile"]["hash"]) == str, "user_hash возвращается в некорректном формате"
            assert get_token_response["profile"]["login"] == self.main_user_login, "Возвращается некорректный login"
            assert get_token_response["profile"][
                       "domain"] == self.main_company_domain, "Возвращается некорректный domain"
            assert get_token_response["profile"][
                       "name"] == self.main_user_name, "Возвращается некорректное имя пользователя"
            assert get_token_response["profile"][
                       "surname"] == self.main_user_surname, "Возвращается некорректное фамилия пользователя"
            assert get_token_response["profile"][
                "avatars"], "Не возвращается аватарки пользователя"
            assert type(get_token_response["profile"][
                            "city"]) == str, "Не возвращается город пользователя"
            try:
                assert get_token_response["profile"][
                           "timezone"] == self.main_user_timezone, "Возвращается некорректный часовой пояс пользователя"
            except AssertionError:
                self.send_info_in_debug_bot(get_token_response["profile"][
                           "timezone"])
            assert get_token_response["profile"][
                       "time_12_hour"] in self.bool_array, "time_12_hour должен иметь значение bool"
            assert get_token_response["profile"][
                       "timezone_manual"] in self.bool_array, "timezone_manual должен иметь значение bool"
            assert get_token_response["profile"][
                       "city_manual"] in self.bool_array, "city_manual должен иметь значение bool"
            assert get_token_response["profile"][
                       "company_id"] == self.main_company_id, "Возвращается неккоретный айди компании"
            assert get_token_response["profile"][
                       "role"] == self.main_user_role, "Возвращается некорректная роль участника в компании"
            assert get_token_response["profile"][
                       "status"] == self.main_user_status, "Возвращается некорректный статус участника в компании"
            assert get_token_response["profile"][
                "settings"], "Не возвращаются настройки пользователя"
        elif status_code == 401:
            get_token_request = requests.get(f"{self.main_api_url}/login", json=self.base_json())
            assert get_token_request.status_code == 401, "Не возвращается 401 ответ при запросе без токена авторизации"
            assert get_token_request.json()[
                       "errMsg"] == self.no_auth_error2, "Не возвращается ошибка при запросе без токена авторизации"

    def delete_login(self, status_code: int = 200):
        if status_code == 200:
            delete_login_request = requests.delete(f"{self.main_api_url}/login",
                                                   headers=self.get_headers(self.test_user_token_url),
                                                   json=self.base_json())
            assert delete_login_request.status_code == 200, "Не работает запрос"
            assert delete_login_request.json()["response"] == True, "Не возвращается True при выполнении запроса"
        elif status_code == 401:
            delete_login_request = requests.delete(f"{self.main_api_url}/login",
                                                   json=self.base_json())
            assert delete_login_request.status_code == 401, "Не возвращается 401 ответ при запросе без токена авторизации"
            assert delete_login_request.json()[
                       "errMsg"] == self.no_auth_error, "Не возвращается ошибка при запросе без токена авторизации"
        else:
            pytest.fail(f"На такой запрос кода ({status_code}) проверка отсутствует.")


    def get_jwt_token(self, status_code: int = 200, check: bool = True):
        if status_code == 200:
            get_jwt_token_request = requests.get(f"{self.main_api_url}/login/get",
                                                 headers=self.get_headers(self.main_user_token_url),
                                                 json=self.base_json())
            if check:
                assert get_jwt_token_request.status_code == 200, "Запрос не работает"
                assert type(get_jwt_token_request.json()["response"][
                                "token"]) == str, "JWT токен возвращается в неккоректном формате"
                assert type(get_jwt_token_request.json()["response"][
                                "refresh"]) == str, "refresh параметр возвращается в неккоректном формате"
                assert get_jwt_token_request.json()["response"]["token"] != get_jwt_token_request.json()["response"][
                    "refresh"], 'параметр refresh не должен быть = jwt токену'
            token = get_jwt_token_request.json()["response"]["token"]
            refresh = get_jwt_token_request.json()["response"]["refresh"]
            return [token, refresh]
        elif status_code == 401:
            get_jwt_token_request = requests.get(f"{self.main_api_url}/login/get",
                                                 json=self.base_json())
            assert get_jwt_token_request.status_code == 401, "Не возвращается 401 ответ при запросе без токена авторизации"
            try:
                assert get_jwt_token_request.json()[
                           "errMsg"] == self.no_auth_error, "Не возвращается ошибка при запросе без токена авторизации"
            except AssertionError:
                assert get_jwt_token_request.json()[
                           "errMsg"] == self.no_auth_error2, "Не возвращается ошибка при запросе без токена авторизации"
        elif status_code == 404:
            #Выполнение запроса без JSON
            get_jwt_token_request = requests.get(f"{self.main_api_url}/login/get",
                                                 headers=self.get_headers(self.main_user_token_url))
            assert get_jwt_token_request.status_code == 200, ""
            assert type(get_jwt_token_request.json()["response"][
                            "token"]) == str, "JWT токен возвращается в неккоректном формате"
            assert type(get_jwt_token_request.json()["response"][
                            "refresh"]) == str, "refresh параметр возвращается в неккоректном формате"
            assert get_jwt_token_request.json()["response"]["token"] != get_jwt_token_request.json()["response"][
                "refresh"], 'параметр refresh не должен быть = jwt токену'

    def refresh_jwt_token(self, refresh: str, previous_token: str, status_code: int = 200):
        if status_code == 200:
            refresh_jwt_request = requests.get(f"{self.main_api_url}/login/refresh",
                                               headers=self.get_headers(self.main_user_token_url),
                                               json=self.json_for_refresh_jwt(refresh))
            assert refresh_jwt_request.status_code == 200, "Не работает запрос"
            actual_token = refresh_jwt_request.json()["response"]["token"]
            assert actual_token != previous_token, "JWT токен не обновляется после запроса"
            assert type(refresh_jwt_request.json()["response"][
                            "refresh"]) == str, ""
        elif status_code == 401:
            refresh_jwt_request = requests.get(f"{self.main_api_url}/login/refresh",
                                               json=self.json_for_refresh_jwt(refresh))
            assert refresh_jwt_request.status_code == 401, "Не возвращается 401 ответ при запросе без токена авторизации"
            try:
                assert refresh_jwt_request.json()[
                           "errMsg"] == self.no_auth_error, "Не возвращается ошибка при запросе без токена авторизации"
            except AssertionError:
                assert refresh_jwt_request.json()[
                           "errMsg"] == self.no_auth_error2, "Не возвращается ошибка при запросе без токена авторизации"



    def email_availability_check(self, hash_registration: (str, None), email: (str, None), status_code: int = 200):
        if status_code == 200:
            email_availability_request = requests.post(
                f"{self.main_api_url}/login/create/{hash_registration}/check_email",
                headers=self.get_headers(self.main_user_token_url),
                json=self.json_for_email_availability(registration_hash=hash_registration, email=email))

    def get_login_list(self, status_code: int = 200):
        if status_code == 200:
            get_login_list_request = requests.get(f"{self.main_api_url}/login/list",
                                                  headers=self.get_headers(self.main_user_token_url),
                                                  json=self.base_json())
            get_login_list_response = get_login_list_request.json()["response"]["profile"]
            x = 0
            while x < 10000:
                try:
                    assert type(
                        get_login_list_response[x]["hash"]) == str, "hash юзера возвращается в неккоректном формате"
                    assert type(
                        get_login_list_response[x]["name"]) == str, "имя юзера возвращается в неккоректном формате"
                    assert type(get_login_list_response[x][
                                    "surname"]) == str, "фамилия юзера возвращается в неккоректном формате"
                    assert type(
                        get_login_list_response[x]["login"]) == str, "login юзера возвращается в неккоректном формате"
                    assert type(
                        get_login_list_response[x]["domain"]) == str, "домен юзера возвращается в неккоректном формате"
                    try:
                        assert get_login_list_response[x]["avatar"].__contains__(
                            self.avatar_server_url), "Не возвращается аватарка пользователя"
                    except AssertionError:
                        assert get_login_list_response[x]["avatar"] == '', "Не возвращается аватарка пользователя"
                    assert get_login_list_response[x][
                               "status"] in self.user_status_array, "Не возвращается статус пользователя"
                    try:
                        assert get_login_list_response[x]["last_message_at"] is None, "Не возвращается last_message_at"
                    except AssertionError:
                        assert type(get_login_list_response[x][
                                        "last_message_at"]) == int, "last_message_at возврващется в неккоректном формате"
                    try:
                        assert get_login_list_response[x]["company_avatar"].__contains__(
                            self.avatar_server_url), "Не возвращается аватарка пользователя"
                    except AssertionError:
                        assert get_login_list_response[x][
                                   "company_avatar"] == '', "Не возвращается аватарка пользователя"
                    x += 1
                except (IndexError, KeyError):
                    assert x != 1, "Возвращается только 1 компания"
                    assert x > 1000, "Должно возвращаться больше 1000 компаний"
                    break
        elif status_code == 401:
            get_login_list_request = requests.get(f"{self.main_api_url}/login/list",
                                                  json=self.base_json())
            assert get_login_list_request.status_code == 401, "Не возвращается 401 ответ при запросе без токена авторизации"
            assert get_login_list_request.json()[
                       "errMsg"] == self.no_auth_error, "Не возвращается ошибка в теле ответа при запросе без токена авторизации"

    def get_code(self, phone: (None, str), email: (str, None), status_code: int = 200):
        if status_code == 200:
            get_code_request = requests.post(f"{self.main_api_url}/login/code",
                                             headers=self.get_headers(self.main_user_token_url),
                                             json=self.json_for_get_code(phone, email))
            assert get_code_request.status_code == 200, "Запрос не работает"
            assert get_code_request.json()["response"]["send"] == True, "Не работает запрос на получение кода"
        elif status_code == 401:
            #Headers are empty
            get_code_request = requests.post(f"{self.main_api_url}/login/code",
                                             json=self.json_for_get_code(phone, self.generate_email()))
            assert get_code_request.status_code == 200, "Запрос не работает без авторизации"
            assert get_code_request.json()["response"][
                       "send"] == True, "Не работает запрос на получение кода без авторизации"
        elif status_code == 404:
            get_code_request = requests.post(f"{self.main_api_url}/login/code",
                                             headers=self.get_headers(self.main_user_token_url),
                                             json=self.json_for_get_code(None, email))
            assert get_code_request.status_code == 200, "Запрос не работает"
            assert get_code_request.json()["response"]["send"] == True, "Не работает запрос на получение кода"
            get_code_request = requests.post(f"{self.main_api_url}/login/code",
                                             headers=self.get_headers(self.main_user_token_url),
                                             json=self.json_for_get_code(phone, None))
            assert get_code_request.status_code == 200, "Запрос не работает"
            assert get_code_request.json()["errMsg"] == "empty phone or email"
            get_code_request = requests.post(f"{self.main_api_url}/login/code",
                                             headers=self.get_headers(self.main_user_token_url),
                                             json=self.json_for_get_code(None, None))
            assert get_code_request.json()[
                       "errMsg"] == "empty phone or email", "Не возвращается ошибка при запросе с пустой почтой или номером телефона"

    def put_code(self, phone: (None, str), email: (str, None), code: (int, None), hash_invite: (None, str),
                 status_code: int = 200):
        if status_code == 200:
            put_code_request = requests.put(f"{self.main_api_url}/login/code",
                                            headers=self.get_headers(self.main_user_token_url),
                                            json=self.json_for_verification_code(phone=phone, email=email, code=code,
                                                                                 hash_invite=hash_invite))
