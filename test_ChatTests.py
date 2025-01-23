import pytest
from Chat.ChatRequests import Chat


def test_get_chat():
    chat = Chat()
    chat.get_chat_information(status_code=200, chat_hash=chat.test_chat_hash, headers=chat.get_headers(chat.main_user_token_url))

@pytest.mark.get_popular_chats
def test_get_popular_chats():
    chat = Chat()
    chat.get_popular_chats(status_code=200,
                           headers=chat.get_headers(chat.main_user_token_url))
    chat.get_popular_chats(status_code=401,
                           headers=None)
    chat.get_popular_chats(headers=chat.get_headers(chat.main_user_token_url))

@pytest.mark.chat_list_count
def test_chat_list_count():
    chat = Chat()
    # Запрос на кол-во чатов(Без архивных)
    chat.get_chat_list_count(status_code=200, headers=chat.get_headers(chat.main_user_token_url), is_archive=True)
    # Запрос на кол-во только архивных чатов
    chat.get_chat_list_count(status_code=200, headers=chat.get_headers(chat.main_user_token_url), is_archive=False)
    # Запрос на кол-во чатов без указания параметра is_archive. Должен возвращать кол-во обычных чатов
    chat.get_chat_list_count(status_code=200, headers=chat.get_headers(chat.main_user_token_url), is_archive=None)
    # Запрос на кол-во чатов без авторизации
    chat.get_chat_list_count(status_code=401, headers=chat.get_headers(chat.main_user_token_url), is_archive=True)

@pytest.mark.get_available_channel_list_count
def test_get_available_channel_list_count():
    chat = Chat()
    chat.get_available_channel_list_count(status_code = 200, headers=chat.get_headers(chat.main_user_token_url))
    chat.get_available_channel_list_count(status_code = 401, headers=chat.get_headers(chat.main_user_token_url))

@pytest.mark.get_chats_allow_for_invite
def test_get_chats_allow_for_invite():
    chat = Chat()
    chat.get_chats_allow_for_invite(status_code = 200, headers=chat.get_headers(chat.main_user_token_url))
    chat.get_chats_allow_for_invite(status_code = 401, headers=None)

@pytest.mark.rename_chat
def test_rename_chat():
    chat = Chat()
    # Запрос корректными входящими данными
    chat.rename_chat(status_code = 200,
                     headers=chat.get_headers(chat.main_user_token_url),
                     new_title=chat.generate_random_string(10),
                     chat_hash=None, available_hash=True)
    # Запрос с хэшем чата, где пользователь не имеет права редактировать название
    chat.rename_chat(status_code = 200,
                     headers=chat.get_headers(chat.main_user_token_url),
                     new_title=chat.generate_random_string(10),
                     chat_hash=None, available_hash=False)
    # Запрос без авторизации
    chat.rename_chat(status_code = 401,
                     headers=None,
                     new_title=chat.generate_random_string(10),
                     chat_hash=None, available_hash=False)
    # Запрос без хэша чата
    chat.rename_chat(status_code = 404,
                     headers=chat.get_headers(chat.main_user_token_url),
                     new_title=chat.generate_random_string(10),
                     chat_hash=None, available_hash=None)
    # Запрос без ожидаемого title чата
    chat.rename_chat(status_code = 404,
                     headers=chat.get_headers(chat.main_user_token_url),
                     new_title=None,
                     chat_hash=None, available_hash=True)







