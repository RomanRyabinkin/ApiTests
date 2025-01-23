from typing import Optional
from BaseDirectory.BaseModule import test_chat_hash, api_version
from ChatGet.DateFunction import utc_mark

json_for_get_chat = {
    "hash": test_chat_hash,
    "version": api_version
}

json_for_topic_list = {
    "limit": 100,
    "offset": 0,
    "version": api_version
}

json_for_over_limit = {
    "limit": 150,
    "offset": 0,
    "version": api_version
}


json_for_syncronization_direct_chats = {
    "date": utc_mark,
    "offset": 100,
    "limit": 100,
    "version": api_version
}

json_for_over_limit_syncronization_direct_chats = {
    "date": utc_mark,
    "offset": 100,
    "limit": 150,
    "version": api_version
}

json_for_syncronization_all_chats = {
    "only_thread": False,
    "date": utc_mark,
    "offset": 100,
    "limit": 100,
    "version": api_version
}

class ChatGetJson:
    @staticmethod
    def json_for_get_users_in_chat(chat_hash: Optional[str] = None, not_in_contact: Optional[bool] = None):
        json = {
            "hash": chat_hash,
            "not_in_contact": not_in_contact,
            "version": api_version
        }
        return json