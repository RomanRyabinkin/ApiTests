from BaseDirectory.BaseModule import Base


class Message(Base):
    def get_unread_messages(self, status_code: int = 200):
        if status_code == 200:
            pass
