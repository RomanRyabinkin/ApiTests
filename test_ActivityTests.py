import pytest

from Activity.ActivityRequests import Activity


@pytest.mark.get_activity
def test_get_activity():
    activity = Activity()
    activity.get_activity()


@pytest.mark.get_activity_hash
def test_get_activity_hash():
    activity = Activity()
    activity.get_activity_hash()