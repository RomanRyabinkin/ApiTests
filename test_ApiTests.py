import pytest
from Auth.AuthRequests import Authorization
from BaseDirectory.BaseModule import BotMessage


@pytest.mark.bot_message
def test_bot_message():
    bot = BotMessage()
    bot.bot_message()


@pytest.mark.sessions_list
def test_sessions_list():
    test = Authorization()
    test.check_auth_list_request()


def test_revoke_authorization():
    test = Authorization()
    test.check_revoke_authorization()


if __name__ == '__main__':
    pytest.run()
