from typing import Optional
from Chat.ChatRequests import Chat


class FolderJson(Chat):
    def json_for_create_folder(self, subject_hash: Optional[str], title: Optional[str], sort: Optional[int]):
        json = {
            "subject_hash": subject_hash,
            "title": title,
            "sort": sort,
            "version": self.api_version
        }
        return json

    def json_for_sort_folder(self, sort: Optional[int] = None, folder_hash: Optional[str] = None):
        json = {
            "sort": sort,
            "hash": folder_hash,
            "version": self.api_version
        }
        return json

    def json_for_rename_folder_title(self, title: Optional[str] = None, folder_hash: Optional[str] = None):
        json = {
            "title": title,
            "hash": folder_hash,
            "version": self.api_version
        }
        return json

