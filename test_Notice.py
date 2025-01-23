import pytest
from Notice.NoticeRequests import Notice


@pytest.mark.get_notice
def test_get_notice():
    notice = Notice()
    notice.get_notice(200)
    notice.get_notice(401)

@pytest.mark.get_one_notice
def test_get_one_notice():
    notice = Notice()
    notice_id = notice.get_notice(200, only_return_notice_id=True)
    notice.get_one_notice(notice_id)
    notice.get_one_notice(notice_id, status_code=401)
    notice.get_one_notice(notice_id, status_code=404)

@pytest.mark.add_notice
def test_add_notice():
    notice = Notice()
    notice.add_notice_requests()

@pytest.mark.edit_notice
def test_edit_notice():
    notice = Notice()
    notice_data = notice.add_notice_requests()
    notice_id = notice_data[0]
    notice_date = notice_data[1]
    notice.edit_notice(notice_id=notice_id, date=notice_date, description="TEST")
    notice.edit_notice(status_code=401, notice_id=notice_id, date=notice_date, description="TEST")
    notice.edit_notice(status_code=404, notice_id=notice_id, date=notice_date, description="TEST")


@pytest.mark.delete_notice
def test_delete_notice():
    notice = Notice()
    notice_data = notice.add_notice_requests()
    notice_id = notice_data[0]
    notice.delete_notice(notice_id=notice_id, status_code=200)
    notice.delete_notice(notice_id=notice_id, status_code=401)
    notice.delete_notice(notice_id=notice_id, status_code=404)

@pytest.mark.finish_notice
def test_finish_notice():
    notice = Notice()
    notice_data = notice.add_notice_requests()
    notice_id = notice_data[0]
    notice.finish_notice(notice_id)
    notice.finish_notice(notice_id, status_code=401)
    notice.finish_notice(notice_id, status_code=404)



