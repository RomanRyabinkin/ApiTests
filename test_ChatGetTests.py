import pytest
from ChatGet.ChatGetRequests import ChatGet


@pytest.mark.get_chat
def test_get_chat():
    chat = ChatGet()
    chat.chat_information()


@pytest.mark.popular_chats
def test_popular_chats():
    chat = ChatGet()
    chat.popular_chats()


@pytest.mark.get_topics
def test_get_topics():
    chat = ChatGet()
    chat.get_topic_list()


@pytest.mark.directs_chats_synchronization
def test_direct_chats_synchronization():
    chat = ChatGet()
    chat.synchronization_direct_chats_list()

@pytest.mark.get_user_from_chat
def test_get_user_from_chat():
    chat = ChatGet()
    chat.get_users_from_chat(status_code=200, headers=chat.get_headers(chat.main_user_token_url), not_in_contact=False, chat_hash="141f6379-9ba4-4462-b37e-1803680b7c20")
    chat.get_users_from_chat(status_code=200, headers=chat.get_headers(chat.main_user_token_url), not_in_contact=True, chat_hash="141f6379-9ba4-4462-b37e-1803680b7c20")
    chat.get_users_from_chat(status_code=200, headers=chat.get_headers(chat.main_user_token_url), not_in_contact=None, chat_hash="141f6379-9ba4-4462-b37e-1803680b7c20")
    chat.get_users_from_chat(status_code=401, headers=None, not_in_contact=None, chat_hash="141f6379-9ba4-4462-b37e-1803680b7c20")
    chat.get_users_from_chat(status_code=404, headers=chat.get_headers(chat.main_user_token_url), not_in_contact=None, chat_hash=None)



if __name__ == '__main__':
    pytest.run()
