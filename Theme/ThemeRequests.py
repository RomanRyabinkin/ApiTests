import requests

from Auth.AuthJson import json_for_api_version
from BaseDirectory.BaseModule import main_api_url, main_headers


class Theme:
    def get_theme_base_color(self):
        """Корректный запрос"""
        theme_base_color_request = requests.get(f"{main_api_url}/theme.getbaseColorName", json=json_for_api_version, headers=main_headers)
        print(theme_base_color_request.json())
        assert theme_base_color_request.status_code == 200
        def all_theme_check(theme):
            assert theme_base_color_request.json()["response"].__contains__(theme)
        all_theme_check("orange_1")
        all_theme_check("yellow_1")
        all_theme_check("green_1")
        all_theme_check("blue_1")
        all_theme_check("red_1")
        all_theme_check("purple_1")
        all_theme_check("pink_1")
        all_theme_check("coral_1")
        all_theme_check("grey_1")
        """Неккоректный запрос(Нет заголовков/Авторизации)"""
        no_headers_request = requests.get(f"{main_api_url}/theme.getbaseColorName", json=json_for_api_version)
        assert no_headers_request.status_code == 401
        assert no_headers_request.json()["errMsg"] == "NOT_FOUND_AUTH"
        """Неккоретный запрос(Без входящего параметра версии API. Запрос должен пройти успешно)"""
        no_json_request = requests.get(f"{main_api_url}/theme.getbaseColorName", headers=main_headers)
        assert no_json_request.status_code == 200
        assert no_json_request.json()["response"].__contains__("orange_1")