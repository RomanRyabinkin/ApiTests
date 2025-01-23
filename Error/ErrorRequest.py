import requests

from Auth.AuthJson import json_for_api_version
from BaseDirectory.BaseModule import main_api_url, main_headers


class Error:
    def error_request(self):
        """Корректный запрос"""
        error = requests.post(f"{main_api_url}/error", headers=main_headers, json=json_for_api_version)
        assert error.status_code == 404
        print(error.json())
        assert error.json()["errMsg"] == "Not found method"
        """Неккоретный запрос(Нет заголовков/Авторизации"""
        no_headers_error = requests.post(f"{main_api_url}/error", json=json_for_api_version)
        print(no_headers_error.json())
        assert no_headers_error.status_code == 404
        assert no_headers_error.json()["errMsg"] == "Not found method"
        """Неккоректный запрос(Без указания API версии). Запрос должен пройти"""
        error = requests.post(f"{main_api_url}/error", headers=main_headers)
        assert error.status_code == 404
        assert error.json()["errMsg"] == "Not found method"
