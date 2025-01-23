import pytest
from Company.CompanyRequests import Company


@pytest.mark.company_banner_info
def test_company_banner_info():
    company = Company()
    company.invite_banner_info()


@pytest.mark.put_invite_banner
def test_put_invite_banner():
    company = Company()
    company.put_invite_banner()


@pytest.mark.count_company_users
def test_count_company_users():
    company = Company()
    company.company_count_users_info()


@pytest.mark.company_info
def test_company_info():
    company = Company()
    company.company_info()


if __name__ == '__main__':
    pytest.run()
