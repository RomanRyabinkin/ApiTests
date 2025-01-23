from typing import Optional

import requests
import json

from Date.DateFunctions import Date

last_version = "1.18"
api_version = "0.7"
get_token_url1 = "https://api.lenzaos.com/login/custom_auth?v=0.5&access=pc2bMZemryBvTMVBJKCF6iBaIvLfY1vG31ubgSYx"
get_token_url2 = "https://api.lenzaos.com/login/custom_auth?access=o27erm0LfOI86HUsXclWBE7G6nhAxsw7p3jplBOI"
main_api_url = "https://api.lenzaos.com"
file_server_url = "https://avatars.lenzaos.com"
bot_message_request_url = "https://api.lenzaos.com/integration/webhook/qNB_Gk4oz18URK6z56a305dmF34o26F0569uY5P"
bot_json = {"message": f"API Тесты были запущены на версии: {api_version}"}
test_chat_hash = "233c5787-7ff1-452b-ad44-a8b38c8c94e5"


def get_headers(token_url):
    request1 = requests.get(token_url)
    token1 = request1.json()["response"]["token"]
    hash1 = request1.json()["response"]["profile"]["hash"]
    headers1 = {'token': token1, 'hash': hash1}
    return headers1


main_headers = get_headers(token_url=get_token_url1)
test_headers = get_headers(token_url=get_token_url2)


class BotMessage:
    def bot_message(self):
        requests.post(bot_message_request_url, json=bot_json, headers=main_headers)


class Base(Date):
    def __init__(self):
        super().__init__()
        self.last_version = "1.18"
        self.api_version = "0.7"
        self.main_user_token_url = "https://api.lenzaos.com/login/custom_auth?v=0.5&access=pc2bMZemryBvTMVBJKCF6iBaIvLfY1vG31ubgSYx"
        self.test_user_token_url = "https://api.lenzaos.com/login/custom_auth?access=o27erm0LfOI86HUsXclWBE7G6nhAxsw7p3jplBOI"
        self.main_api_url = "https://api.lenzaos.com"
        self.avatar_server_url = "https://avatars.lenzaos.com"
        self.bot_message_request_url = "https://api.lenzaos.com/integration/webhook/qNB_Gk4oz18URK6z56a305dmF34o26F0569uY5P"
        self.bot_json = {"message": f"API Тесты были запущены на версии: {api_version}"}
        self.test_chat_hash = "233c5787-7ff1-452b-ad44-a8b38c8c94e5"
        self.files_server_url = "https://files.lenzaos.com"
        self.hash_length = 36
        self.test_user_name = "Testik"
        self.test_user_surname = "Testov"
        self.full_test_user_name = "Testik Testov"
        self.test_user_name_login = "testik_testov"
        self.test_user_company_domain = "testik-1"
        self.no_auth_error = "NOT_FOUND_AUTH"
        self.no_auth_error2 = "NOT_AUTH"
        self.not_found_methods_error = "Not found method"
        self.main_company_domain = "hello_world123"
        self.bot_for_debug_token = "hEM_7q9CIPFlHT60l4Gf4h408U20d821Y41S05f"
        self.not_access_error = "not access"
        self.main_user_name = "Roman"
        self.main_user_surname = "Ryabinkin"

    def get_headers(self, token_url):
        request1 = requests.get(token_url)
        token1 = request1.json()["response"]["token"]
        hash1 = request1.json()["response"]["profile"]["hash"]
        headers1 = {'token': token1, 'hash': hash1}
        return headers1

    def base_json(self):
        json = {
            "version": self.api_version
        }
        return json

    def send_info_in_debug_bot(self, message: str):
        json_for_bot = {
            "token": self.bot_for_debug_token,
            "version": self.api_version,
            "message": message
        }
        requests.post(f"{self.main_api_url}/integration/webhook/{self.bot_for_debug_token}", json=json_for_bot, headers=main_headers)


    @staticmethod
    def generate_random_string(length: Optional[int] = 10):
        import random
        import string
        characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
        return ''.join(random.choices(characters, k=length))

    @staticmethod
    def generate_random_number(start_number: Optional[int], end_number: Optional[int]):
        import random
        return random.randint(start_number, end_number)

