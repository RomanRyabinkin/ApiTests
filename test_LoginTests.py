import pytest
from Login.LoginRequests import Login


@pytest.mark.get_login
def test_get_login():
    login = Login()
    login.get_login()
    login.get_login(status_code=401)


@pytest.mark.delete_login
def test_delete_login():
    login = Login()
    login.delete_login()
    login.delete_login(status_code=401)



def test_get_jwt_token():
    login = Login()
    login.get_jwt_token()
    login.get_jwt_token(status_code=401)
    login.get_jwt_token(status_code=404)


def test_refresh_jwt_token():
    login = Login()
    refresh_param = login.get_jwt_token()[1]
    jwt_token = login.get_jwt_token()[0]
    login.refresh_jwt_token(refresh=refresh_param, previous_token=jwt_token)
    login.refresh_jwt_token(status_code=401, refresh=refresh_param, previous_token=jwt_token)





def test_email_availability():
    login = Login()
    registration_hash = login.create_hash_registration(False)
    login.email_availability_check(hash_registration=registration_hash, email="r0main.ryabinkin@yandex.ru")


@pytest.mark.login_list
def test_login_list():
    login = Login()
    login.get_login_list()
    login.get_login_list(status_code=401)



@pytest.mark.get_code
def test_get_code():
    login = Login()
    login.get_code("89376006973", "r0main.ryabinkin@yandex.ru")
    login.get_code(login.get_phone(), login.generate_email(), 401)
    login.get_code(login.get_phone(), login.generate_email(), 404)


def test_put_code():
    login = Login()
    login.put_code(phone="89376006973", email="r0main.ryabinkin@yandex.ru", code=111111, hash_invite=None)
