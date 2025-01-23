from typing import Optional
from BaseDirectory.BaseModule import Base


class UserJson(Base):
    def json_for_get_user_list(self, timestamp: Optional[int] = None):
        if timestamp is None:
            timestamp = self.current_unix_timestamp
        json = {
            "date": timestamp,
            "version": self.api_version
        }
        return json

    def json_for_get_user(self, user_hash: Optional[str] = None):
        json = {
            "hash": user_hash,
            "version": self.api_version
        }
        return json

    

