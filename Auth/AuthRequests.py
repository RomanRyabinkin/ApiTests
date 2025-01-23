import requests

from BaseDirectory.BaseModule import api_version, Base
from BaseDirectory.BaseModule import main_headers
from BaseDirectory.BaseModule import test_headers
from BaseDirectory.BaseModule import main_api_url
from Auth.AuthJson import json_for_used_domain
from Auth.AuthJson import json_for_unused_domain
from Auth.AuthJson import json_for_api_version
from Auth.AuthFunctions import uncorrect_domain_name
from Auth.AuthFunctions import fake_headers




class Authorization(Base):

    def check_auth_list_request(self):
        auth_list_request = requests.get(f"{main_api_url}/auth.list?v={api_version}", json_for_api_version, headers=main_headers)
        if auth_list_request.status_code == 504:
            self.send_info_in_debug_bot("Запрос /auth.list вернул код 504")
        else:
            assert auth_list_request.status_code == 200
            assert auth_list_request.json()["response"]["item"][0]["location"]
            auth_list_request2 = requests.get(f"{main_api_url}/auth.list?v={api_version}", json_for_api_version,
                                              headers=test_headers)
            assert auth_list_request2.status_code == 200
            assert auth_list_request.json()["response"]["item"][0]["location"]
            """Неккоректный запрос"""
            auth_list_request3 = requests.get(f"{main_api_url}/lenza/auth.geoLocal?v={api_version}",
                                              json=json_for_api_version, headers=fake_headers)
            assert auth_list_request3.json()['errMsg'] == "Not found method"
            assert auth_list_request3.status_code == 404
            """Парсинг id сессии"""
            authorization_id = auth_list_request.json()["response"]["item"][0]["id"]
            return authorization_id

    def check_revoke_authorization(self):
        revoke_authorization = requests.get(f"{main_api_url}/auth.revoke?v={api_version}", json=json_for_revoke_session, headers=main_headers)
        print(revoke_authorization.json())



















