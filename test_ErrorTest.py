import pytest

from Error.ErrorRequest import Error


@pytest.mark.error
def test_error():
    error = Error()
    error.error_request()
