from BaseDirectory.BaseModule import Base


class NoticeJson(Base):
    def json_for_one_notice(self, notice_id: str):
        json = {
            "id": notice_id,
            "version": self.api_version
        }
        return json

    def json_for_add_notice(self, timestamp: (int, None), description: (str, None), subject_hash: (str, None), is_important: (bool, None)):
        json = {
            "description": description,
            "date": timestamp,
            "subject_hash": subject_hash,
            "is_important": is_important,
            "version": self.api_version
        }
        return json

    def json_for_edit_notice(self, notice_id: (None, str), date: (None, int), description: (str, None)):
        json = {
            "id": notice_id,
            "description": description,
            "date": date,
            "version": self.api_version
        }
        return json
