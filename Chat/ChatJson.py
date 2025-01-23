from typing import Optional

from ChatGet.ChatGetRequests import ChatGet


class ChatJson(ChatGet):
    def json_for_get_chat_info(self, chat_hash: Optional[str] = None):
        json = {
            "hash": chat_hash,
            "version": self.api_version
        }
        return json

    def json_for_get_chat_list_count(self, is_archive: Optional[bool] = None):
        json = {
            "is_archive": is_archive,
            "version": self.api_version
        }
        return json

    def json_for_rename_chat_name(self, hash_chat: Optional[str] = None,
                                  title: Optional[str] = None):
        json = {
            "hash": hash_chat,
            "title": title,
            "version": self.api_version
        }
        return json
