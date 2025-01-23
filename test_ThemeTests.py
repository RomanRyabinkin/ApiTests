import pytest

from Theme.ThemeRequests import Theme


@pytest.mark.get_theme_base_color
def test_get_theme_base_color():
    theme = Theme()
    theme.get_theme_base_color()