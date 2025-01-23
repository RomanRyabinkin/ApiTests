import requests
import pytest

from Auth.AuthFunctions import random_domain_name, fake_headers
from Auth.AuthJson import json_for_api_version
from BaseDirectory.BaseModule import main_api_url, main_headers


class Company:
    def invite_banner_info(self):
        """Корректный запрос"""
        invite_banner = requests.get(f"{main_api_url}/company/banner/invite", headers=main_headers, json=json_for_api_version)
        assert invite_banner.status_code == 200
        assert invite_banner.json()["response"].__contains__("shown")
        """Неккоректный запрос(Пустые Заголовки/Нет авторизации)"""
        no_auth_invite_banner_info = requests.get(f"{main_api_url}/company/banner/invite", json=json_for_api_version)
        assert no_auth_invite_banner_info.status_code == 401
        assert no_auth_invite_banner_info.json()["errMsg"] == "NOT_FOUND_AUTH"
        """Пустые JSON Параметры(Запрос должен пройти успешно, так как в данном запросе всего 1 параметр: Версия API)"""
        no_json_invite_banner_info = requests.get(f"{main_api_url}/company/banner/invite", headers=main_headers)
        assert no_json_invite_banner_info.status_code == 200
        assert no_json_invite_banner_info.json()["response"].__contains__("shown")

    def put_invite_banner(self):
        """Корректный запрос"""
        put_invite_banner_info = requests.put(f"{main_api_url}/company/banner/invite", json=json_for_api_version, headers=main_headers)
        print(put_invite_banner_info.json())
        assert put_invite_banner_info.status_code == 200
        assert put_invite_banner_info.json()["response"] == True
        """Неккоректный запрос(Пустые Заголовки/Нет авторизации)"""
        no_auth_put_invite_banner_info = requests.put(f"{main_api_url}/company/banner/invite", json=json_for_api_version)
        assert no_auth_put_invite_banner_info.status_code == 401
        assert no_auth_put_invite_banner_info.json()["errMsg"] == "NOT_FOUND_AUTH"
        """Пустые JSON Параметры(Запрос должен пройти успешно, так как в данном запросе всего 1 параметр: Версия API)"""
        no_json_put_invite_banner_info = requests.put(f"{main_api_url}/company/banner/invite", headers=main_headers)
        assert no_json_put_invite_banner_info.status_code == 200
        assert no_json_put_invite_banner_info.json()["response"] == True

    def company_count_users_info(self):
        """Корректный запрос"""
        count_users_info = requests.get(f"{main_api_url}/company/count/user", json=json_for_api_version, headers=main_headers)
        print(count_users_info.json())
        assert count_users_info.status_code == 200
        assert count_users_info.json()["response"]["count"] >= 2
        """"Неккоректный запрос(Пустые Заголовки/Нет авторизации)"""
        no_auth_count_users_info = requests.get(f"{main_api_url}/company/count/user", json=json_for_api_version)
        assert no_auth_count_users_info.status_code == 401
        assert no_auth_count_users_info.json()["errMsg"] == "NOT_FOUND_AUTH"
        """Пустые JSON Параметры(Запрос должен пройти успешно, так как в данном запросе всего 1 параметр: Версия API)"""
        no_json_count_users_info = requests.get(f"{main_api_url}/company/count/user", headers=main_headers)
        assert no_json_count_users_info.status_code == 200
        assert no_json_count_users_info.json()["response"]["count"] >= 2


    def company_info(self):
        """Корректный запрос"""
        def company_name_request(company_name, headers):
            company_info = requests.get(f"{main_api_url}/company/info/{company_name}", headers=headers, json=json_for_api_version)
            return company_info
        result = company_name_request(company_name="lenza", headers=main_headers)
        hello_world_result = company_name_request(company_name="hello_world123", headers=main_headers)
        assert hello_world_result.json()["response"]["domain"] == "hello_world123"
        assert result.json()["response"]["title"] == "Lenza"
        """Неккоретный запрос(Несуществующая компания)"""
        invalid_name = company_name_request(company_name=random_domain_name, headers=main_headers)
        assert invalid_name.status_code == 200
        assert invalid_name.json()["errMsg"] == "value is null"
        """Неккоректный запрос(Нет заголовков/Нет авторизации). Должен быть 400-ый ответ о том, что не удалось найти компанию."""
        no_auth_company_info = company_name_request(company_name="Lenza", headers=fake_headers)
        assert no_auth_company_info.status_code == 200
        assert no_auth_company_info.json()["errMsg"] == "value is null"









