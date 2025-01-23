
from typing import Optional
import requests

from Section.SectionRequests import chat_hash
from User.UserJson import UserJson


class User(UserJson):
    # Получение списка пользователей
    def get_user_list(self, data, status_code: Optional[int] = 200):
        from datetime import timedelta
        # Выполнение запроса со вчерашней меткой
        if status_code == 200:
            response = requests.get(f"{self.main_api_url}/user", json=self.json_for_get_user_list(timestamp=int((self.current_data - timedelta(days=1)).timestamp())), headers=self.get_headers(self.main_user_token_url))
            assert response.status_code == 200, "Запрос не возвращает 200 статус"
            # Проверка, что возвращаемые поля не пустые
            def check_fields(data = None):
                required_fields = ['login', 'last_online', 'status', 'emoji_status', 'contact_status', 'timezone']
                for field in required_fields:
                    if field not in data:
                        if field not in data or not data[field]:
                            return False

                    return True
                # Пример данных
                if data is None:
                    data = {
                        'login': 'user123',
                        'last_online': '2025-01-15 10:00:00',
                        'status': 'online',
                        'emoji_status': '🙂',
                        'contact_status': 'active',
                        'timezone': 'UTC+3'
                    }

                # Вызов функции
                check_fields(data)

    def get_user_profile(self,
                         status_code: Optional[int] = None,
                         headers: Optional[dict] = None,
                         user_hash: Optional[str] = None,
                         available_hash: Optional[bool] = True):
        if status_code == 200:
            if available_hash is True and user_hash is None:
                user_hash = self.get_headers(self.test_user_token_url)["hash"]
            req = requests.get(f"{self.main_api_url}/user/{user_hash}", headers=headers, json=self.json_for_get_user(user_hash))
            if available_hash is True and user_hash is None:
                assert req.status_code == 200, "Запрос не работает"
                assert req.json()["response"]["hash"] == user_hash, "Возвращается некорректный хэш юзера"
                assert req.json()["response"]["login"] == self.test_user_name_login, "Возвращается некорректный логин пользователя"
                assert req.json()["response"]["domain"] == self.test_user_company_domain, "Возвращается некорректный домен пользователя"
                assert type(req.json()["response"]["date_of_registration"]) == int, "Возвращается неккоректный тип данных в дате регистрации пользователя"
                assert isinstance(req.json()["response"]["phone"],
                                  str), "Возвращается некорректный тип данных в номере пользователя"
                assert req.json()["response"]["name"] == self.test_user_name, "Возвращается некорректное имя пользователя"
                assert req.json()["response"]["surname"] == self.test_user_surname, "Возвращается некорректная фамилия пользователя"
                #TODO Дописать проверку на остальные возвращаемые поля
                return [req.json()["response"]["contact_status"]]
            elif user_hash is not None:
                return [req.json()["response"]["contact_status"], req.json()]

        elif status_code == 401:
            if available_hash is True and user_hash is None:
                user_hash = self.get_headers(self.test_user_token_url)["hash"]
            req = requests.get(f"{self.main_api_url}/user/{user_hash}", headers=None,
                               json=self.json_for_get_user(user_hash))
            assert req.status_code == 401, "Не возвращается ошибка при выполнении запроса без авторизации"
            assert req.json()["errMsg"] == self.no_auth_error, "Не возвращается ошибка при выполнении запроса без авторизации"
        elif status_code == 404:
            if user_hash is None and available_hash is False or None:
                user_hash = self.generate_random_string(36)
                req = requests.get(f"{self.main_api_url}/user/{user_hash}", headers=None,
                                   json=self.json_for_get_user(user_hash))
                assert req.status_code == 404, "Не возвращается ошибка при выполнении запроса без указания юзер хэша"
                assert req.json()["errMsg"] == self.not_found_methods_error, "Не возвращается ошибка при выполнении запроса без указания юзер хэша"















