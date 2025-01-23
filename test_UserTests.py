import pytest

from User.UserRequests import User


def test_get_user_list():
    user = User()
    user.get_user_list(data=None)

@pytest.mark.get_user_profile
def test_get_user_profile():
    user = User()
    user.get_user_profile(headers=user.get_headers(user.main_user_token_url), available_hash=True, status_code=200)
    user.get_user_profile(headers=None, status_code=401, available_hash=True)
    user.get_user_profile(headers=user.get_headers(user.main_user_token_url), available_hash=False, status_code=404)

