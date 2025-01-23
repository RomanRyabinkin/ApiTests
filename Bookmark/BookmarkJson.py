from BaseDirectory.BaseModule import test_chat_hash, api_version
from Bookmark.BookmarkFunctions import generate_random_title_name, generate_random_sort_param

add_bookmark_json = {
    "subject_hash": test_chat_hash,
    "title": generate_random_title_name,
    "url": "https://www.youtube.com/",
    "sort": generate_random_sort_param,
    "version": api_version
}



