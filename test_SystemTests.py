import pytest

from System.SystemRequests import System


@pytest.mark.system_health
def test_system_health():
    system = System()
    system.system_health_request()


@pytest.mark.system_last_version
def test_system_last_version():
    system = System()
    system.system_last_version_request()
