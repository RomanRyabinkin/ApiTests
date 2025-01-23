import requests

from Auth.AuthFunctions import fake_headers
from Auth.AuthJson import json_for_api_version
from BaseDirectory.BaseModule import main_api_url, main_headers, test_headers
from Section.SectionJson import sorting_settings_function, add_section_function, edit_section_function, \
    json_for_throw_section
from Section.SectionsFunctions import random_number, random_string
chat_hash = "fa161bbd-ba7d-474a-b033-de538013f035"


class Section:
    def get_sections(self, headers):
        sections = requests.get(f"{main_api_url}/section", headers=headers, json=json_for_api_version)
        sect = sections.json()
        assert sections.status_code == 200
        def section_list_check(count):
            try:
                x = 0
                z = 0
                while x < count:
                    assert sections.json()["response"][x]["items"][z]
                    print(sections.json()["response"][x]["items"][z])
                    print(x)
                x = x + 1
                z = z + 1
            except IndexError:
                print(x)
        """Неккоректный запрос(Нет заголовков/Авторизации"""
        no_auth_secrtion = requests.get(f"{main_api_url}/section", json=json_for_api_version)
        assert no_auth_secrtion.status_code == 401
        assert no_auth_secrtion.json()["errMsg"] == "NOT_FOUND_AUTH"
        """Запрос без взодящих параметров(Запрос должен успешно пройти)"""
        no_json = requests.get(f"{main_api_url}/section", headers=headers)
        assert no_json.status_code == 200
        assert no_json.json()["response"][1]["id"]
        return sect

    def section_settings(self, headers):
        """Корректный запрос. Со всеми параметрами должен приходить 200-ый ответ"""
        def check_settings_sort_sections(sort, show):
            all_sections_settings = requests.put(f"{main_api_url}/section", headers=headers, json=sorting_settings_function(sort=sort, show=show))
            assert all_sections_settings.status_code == 200
            assert all_sections_settings.json()["response"] == True
        check_settings_sort_sections(sort="ALL", show="ALL")
        check_settings_sort_sections(sort="ALL", show="UNREAD")
        check_settings_sort_sections(sort="ALL", show="MENTION")
        check_settings_sort_sections(sort="UNREAD_ABC", show="ALL")
        check_settings_sort_sections(sort="UNREAD_ABC", show="MENTION")
        check_settings_sort_sections(sort="UNREAD_ABC", show="UNREAD")
        check_settings_sort_sections(sort="TIME_ASC", show="MENTION")
        check_settings_sort_sections(sort="TIME_ASC", show="ALL")
        check_settings_sort_sections(sort="TIME_ASC", show="UNREAD")
        check_settings_sort_sections(sort="TIME_ASC", show="ALL")
        check_settings_sort_sections(sort="TIME_ASC", show="MENTION")
        check_settings_sort_sections(sort="TIME_DESC", show="ALL")
        check_settings_sort_sections(sort="TIME_DESC", show="MENTION")
        check_settings_sort_sections(sort="TIME_DESC", show="MENTION")
        check_settings_sort_sections(sort="ABC_ASC", show="UNREAD")
        check_settings_sort_sections(sort="ABC_ASC", show="ALL")
        check_settings_sort_sections(sort="ABC_ASC", show="MENTION")
        check_settings_sort_sections(sort="ABD_DESC", show="ALL")
        check_settings_sort_sections(sort="ABD_DESC", show="UNREAD")
        check_settings_sort_sections(sort="ABD_DESC", show="MENTION")
    """Неккоректный запрос(Отсутствуют хедеры/Нет авторизации)"""
    no_auth_sections_settings = requests.put(f"{main_api_url}/section", json=json_for_api_version)
    # print(no_auth_sections_settings.json())
    # assert no_auth_sections_settings.status_code == 401
    assert no_auth_sections_settings.json()["errMsg"] == "NOT_FOUND_AUTH"
    """Неккоректный запрос(Отсутствуют входящие параметры). Запрос должен выполниться со статусом 200 и отдать False"""
    no_json_sections_settings = requests.put(f"{main_api_url}/section", headers=main_headers)
    assert no_json_sections_settings.status_code == 200
    assert no_json_sections_settings.json()["response"] == False



    def get_section(self):
        """Корректный запрос"""
        section_hash = self.get_sections(headers=main_headers)["response"][0]["id"]
        get_section_request = requests.get(f"{main_api_url}/section/{section_hash}", headers=main_headers, json=json_for_api_version)
        assert get_section_request.status_code == 200
        assert get_section_request.json()["response"]["type"] == "CUSTOM"
        assert get_section_request.json()["response"]["position"]
        """Неккоректный запрос(Использование других хедеров. Запрос должен упасть с 400-ым статусом)"""
        fake_headers_section_request = requests.get(f"{main_api_url}/section/{section_hash}", headers=test_headers, json=json_for_api_version)
        assert fake_headers_section_request.status_code == 200
        assert fake_headers_section_request.json()["errMsg"] == "not found item"
        """Неккоректный запрос(Без заголвков/Авторизации"""
        no_headers_section_request = requests.get(f"{main_api_url}/section/{section_hash}", json=json_for_api_version)
        assert no_headers_section_request.status_code == 401
        assert no_headers_section_request.json()["errMsg"] == "NOT_FOUND_AUTH"
        """Неккоректный запрос(без входящих параметров, т.е. без хэша). Запрос должен отдать 404-ый статус"""
        no_json_section_request = requests.get(f"{main_api_url}/section/hash", headers=main_headers)
        assert no_json_section_request.status_code == 404
        assert no_json_section_request.json()["errMsg"] == "Not found method"

    def add_section(self):
        """Корректный запрос"""
        def add_section_check(title, position, sort, show):
            add_section_request = requests.post(f"{main_api_url}/section", headers=test_headers, json=add_section_function(title, position, sort, show))
            section_hash = add_section_request.json()["response"]["id"]
            section_delete = requests.delete(f"{main_api_url}/section/{section_hash}", headers=test_headers, json=json_for_api_version)
            assert section_delete.status_code == 200
            assert add_section_request.status_code == 200
            assert add_section_request.json()["response"]["id"]
            return add_section_check
        add_section_check(title=f"{random_string(length=15)}", position=random_number(first_number=300, second_number=700), sort="ALL", show="ALL")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="ALL", show="UNREAD")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="ALL", show="MENTION")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="UNREAD_ABC", show="ALL")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="UNREAD_ABC", show="UNREAD")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="UNREAD_ABC", show="MENTION")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="TIME_ASC", show="ALL")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="TIME_ASC", show="UNREAD")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="TIME_ASC", show="MENTION")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="TIME_DESC", show="ALL")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="TIME_DESC", show="UNREAD")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="TIME_DESC", show="MENTION")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="ABC_ASC", show="ALL")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="ABC_ASC", show="UNREAD")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="ABC_ASC", show="MENTION")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="ABD_DESC", show="ALL")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="ABD_DESC", show="UNREAD")
        add_section_check(title=f"{random_string(length=17)}", position=random_number(first_number=350, second_number=1000), sort="ABD_DESC", show="MENTION")
        """Неккоректный запрос(Неверные заголовки)"""
        def fake_headers_section_request(title, position, sort, show):
            no_headers_section_request = requests.post(f"{main_api_url}/section", headers=fake_headers, json=add_section_function(title, position, sort, show))
            assert no_headers_section_request.status_code == 401
            assert no_headers_section_request.json()["errMsg"] == "NOT_AUTH"
        fake_headers_section_request(title=f"{random_string(length=15)}", position=random_number(first_number=300, second_number=700), sort="ALL", show="ALL")
        """Неккоректный запрос(Нет Входящих JSON параметров)"""
        def no_json_section_add_request():
            no_json_section_request = requests.post(f"{main_api_url}/section", headers=fake_headers)
            print(no_json_section_request.json())
            assert no_json_section_request.status_code == 401
            assert no_json_section_request.json()["errMsg"] == "NOT_AUTH"
        no_json_section_add_request()

    def edit_section(self):
        """Получение хэша"""
        section_hash = self.get_sections(headers=test_headers)["response"][0]["id"]
        def correct_edit_section_request(hash, title, position, sort, show):
            """Корректный запрос"""
            edit_section_request = requests.put(f"{main_api_url}/section", headers=test_headers, json=edit_section_function(hash=hash, title=title, position=position, sort=sort, show=show))
            assert edit_section_request.status_code == 200
            assert edit_section_request.json()["response"] == True
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="ALL", show="ALL")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="ALL", show="UNREAD")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="ALL", show="MENTION")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="UNREAD_ABC", show="ALL")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="UNREAD_ABC", show="UNREAD")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="UNREAD_ABC", show="MENTION")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="TIME_ASC", show="ALL")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="TIME_ASC", show="UNREAD")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="TIME_ASC", show="MENTION")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="TIME_DESC", show="ALL")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="TIME_DESC", show="UNREAD")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="TIME_DESC", show="MENTION")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="ABC_ASC", show="ALL")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="ABC_ASC", show="UNREAD")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="ABC_ASC", show="MENTION")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="ABD_DESC", show="ALL")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="ABD_DESC", show="UNREAD")
        correct_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="ABD_DESC", show="MENTION")
        """Неккоретный запрос(Отсутствие входящих JSON параметров). Запрос должен прийти 200-ым, но с ответом False"""
        no_json_edit_section_request = requests.put(f"{main_api_url}/section", headers=main_headers)
        assert no_json_edit_section_request.status_code == 200
        assert no_json_edit_section_request.json()["response"] == False
        """Неккоректный запрос(Неверные заголовки)"""
        def fake_headers_edit_section_request(hash, title, position, sort, show):
            edit_section_request = requests.put(f"{main_api_url}/section", headers=main_headers, json=edit_section_function(hash=hash, title=title, position=position, sort=sort, show=show))
            assert edit_section_request.status_code == 200
        fake_headers_edit_section_request(hash=section_hash, title=random_string(length=14), position=random_number(first_number=300, second_number=1000), sort="TIME_ASC", show="UNREAD")

    def make_section_on_chat(self):
        """Получение хэша секции"""
        section_hash = self.get_sections(headers=test_headers)["response"][0]["id"]
        """Корректный запрос"""
        make_section_request = requests.put(f"{main_api_url}/section/{section_hash}/{chat_hash}", headers=main_headers, json=json_for_api_version)
        assert make_section_request.status_code == 200
        assert make_section_request.json()["response"] == True
        """Неккоректный запрос(С неправильной структурой. Ответ должен быть 400-ым"""
        invalid_make_section_request = requests.put(f"{main_api_url}/section/{chat_hash}/{section_hash}", headers=main_headers, json=json_for_api_version)
        assert invalid_make_section_request.json()["errMsg"] == "not set"
        assert invalid_make_section_request.status_code == 400
        """Запрос без заголовков/Авторизации"""
        no_headers_make_section_request = requests.put(f"{main_api_url}/section/{section_hash}/{chat_hash}", json=json_for_api_version)
        assert no_headers_make_section_request.status_code == 401
        assert no_headers_make_section_request.json()["errMsg"] == "NOT_FOUND_AUTH"
        """Запрос без указания версия API(Запрос должен пройти. Ответ должен быть 200-ым"""
        no_api_make_section_request = requests.put(f"{main_api_url}/section/{section_hash}/{chat_hash}", headers=main_headers)
        assert no_api_make_section_request.status_code == 200
        assert no_api_make_section_request.json()["response"] == True
        """Неккоректный запрос(Неверный метод в запросе). Ответ должен быть 404-ым"""
        fake_method_make_section_request = requests.post(f"{main_api_url}/section/{section_hash}/{chat_hash}", headers=main_headers, json=json_for_api_version)
        assert fake_method_make_section_request.json()["errMsg"] == "Not found method"
        assert fake_method_make_section_request.status_code == 404

    def delete_section_on_chat(self):
        """Полуечние хэша чата"""
        section_hash = self.get_sections(headers=test_headers)["response"][0]["id"]
        """Корректный запрос"""
        delete_section_on_chat_request = requests.delete(f"{main_api_url}/section/{section_hash}", headers=test_headers, json=json_for_api_version)
        print(delete_section_on_chat_request.json())
        print(delete_section_on_chat_request.status_code)
        assert delete_section_on_chat_request.status_code == 200
        assert delete_section_on_chat_request.json()["response"] == True
        """Неккоректный запрос(Неверный метод в запросе). Ответ должен быть 404-ым"""
        fake_method_delete_section_request = requests.post(f"{main_api_url}/section/{section_hash}", headers=main_headers, json=json_for_api_version)
        assert fake_method_delete_section_request.status_code == 404
        assert fake_method_delete_section_request.json()["errMsg"] == "Not found method"
        """Неккоректный запрос(С неправильной структурой. Ответ должен быть 400-ым)"""
        invalid_method_delete_section_request = requests.delete(f"{main_api_url}/{chat_hash}/section", headers=main_headers, json=json_for_api_version)
        print(invalid_method_delete_section_request.json())
        assert invalid_method_delete_section_request.status_code == 400
        # assert invalid_method_delete_section_request.json()["errMsg"] ==

    def throw_off_section_request(self):
        def req(sort_default, show_default):
            response = requests.put(f"{main_api_url}/section/default", headers=main_headers, json=json_for_throw_section(sort_default, show_default))
            assert response.status_code == 200
            print(response.json())
        req(sort_default=True, show_default=True)

    # def delete_my_sections(self):
    #     data = requests.get(f"{main_api_url}/section", headers=main_headers, json=json_for_api_version)
    #     print(data.json())
    #     ids = [item["id"] for item in data.json()["response"]]
    #     print(len(ids))
    #     x = 0
    #     while x < 500:
    #         data = requests.delete(f"{main_api_url}/section/{ids[x]}", headers=main_headers, json=json_for_api_version)
    #         print(data.json())
    #         x = x + 1































