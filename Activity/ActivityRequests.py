import pytest
import requests
from Activity.ActivityJson import get_activity
from BaseDirectory.BaseModule import main_api_url, main_headers


class Activity:
    def get_activity(self):
        """Корректный запрос"""
        def activity_request(type, unread, offset, limit):
            activity = requests.get(f"{main_api_url}/activity", json=get_activity(type=type, unread=unread, offset=offset, limit=limit), headers=main_headers)
            assert activity.status_code == 200
            # assert activity.json()["response"]["items"][1]["id"]
            with pytest.raises(IndexError):
                assert activity.json()["response"]["items"][110]["id"]
                pytest.fail("Список событий больше 100")
            """Проверка на то, что не может отдаваться больше 100 событий"""
        activity_request(type="all", unread=False, offset=0, limit=100)
        activity_request(type="MENTION", unread=False, offset=0, limit=100)
        activity_request(type="THREAD", unread=False, offset=0, limit=100)
        activity_request(type="REACTION", unread=False, offset=0, limit=100)
        activity_request(type="APPLICATION", unread=False, offset=0, limit=100)
        activity_request(type="all", unread=True, offset=0, limit=100)
        activity_request(type="MENTION", unread=True, offset=0, limit=100)
        activity_request(type="THREAD", unread=True, offset=0, limit=100)
        activity_request(type="REACTION", unread=True, offset=0, limit=100)
        activity_request(type="APPLICATION", unread=True, offset=0, limit=100)
        activity_request(type="all", unread=False, offset=0, limit=150)
        activity_request(type="MENTION", unread=False, offset=0, limit=150)
        activity_request(type="THREAD", unread=False, offset=0, limit=150)
        activity_request(type="REACTION", unread=False, offset=0, limit=150)
        activity_request(type="APPLICATION", unread=False, offset=0, limit=150)
        activity_request(type="all", unread=True, offset=0, limit=150)
        activity_request(type="MENTION", unread=True, offset=0, limit=150)
        activity_request(type="THREAD", unread=True, offset=0, limit=150)
        activity_request(type="REACTION", unread=True, offset=0, limit=150)
        activity_request(type="APPLICATION", unread=True, offset=0, limit=150)
        """Неккоректный запрос(Нет заголовков/Авторизации)"""
        no_headers_req = requests.get(f"{main_api_url}/activity", json=get_activity(type="all", unread=True, offset=0, limit=100))
        assert no_headers_req.status_code == 401
        assert no_headers_req.json()["errMsg"] == "NOT_FOUND_AUTH"
        """Неккоректный запрос(без входящих JSON параметров)"""
        no_json_req = requests.get(f"{main_api_url}/activity", headers=main_headers)
        assert no_json_req.status_code == 200
        assert no_json_req.json()["response"]["items"][0]["id"]
        return no_json_req.json()["response"]["items"][0]["id"]

    def get_activity_hash(self):
        no_json_req = requests.get(f"{main_api_url}/activity", headers=main_headers)
        hash = no_json_req.json()["response"]["items"][0]["id"]
        """Корректный запрос"""
        activity_hash_request = requests.get(f"{main_api_url}/activity/{hash}", headers=main_headers)
        assert activity_hash_request.status_code == 200
        assert activity_hash_request.json()["response"]["item"]["id"]
        """Неккоректный запрос(Нет заголовков/Авторизации)"""
        no_json_req = requests.get(f"{main_api_url}/activity/{hash}")
        assert no_json_req.status_code == 401
        assert no_json_req.json()["errMsg"] == "NOT_FOUND_AUTH"




