import pytest
from Search.SearchRequests import Search


@pytest.mark.global_search
def test_search():
    search = Search()
    search.global_search()


def test_search_in_chat():
    search = Search()
    search.full_search_in_chat()
