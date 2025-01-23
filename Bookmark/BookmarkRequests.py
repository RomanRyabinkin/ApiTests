import requests
from BaseDirectory.BaseModule import main_api_url, main_headers
from Bookmark.BookmarkJson import add_bookmark_json


class Bookmark:
    """Корректный запрос"""
    def add_bookmark(self):
        bookmark_request = requests.post(f"{main_api_url}/bookmark", headers=main_headers, json=add_bookmark_json)
        print(bookmark_request.status_code)
        print(bookmark_request.json())
