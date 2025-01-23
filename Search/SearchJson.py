from BaseDirectory.BaseModule import Base


class SearchJson(Base):
    def search_json(self, s: str, offset: int, limit: int, search_type: str):
        if search_type != "ALL":
            json = {
                "s": s,
                "offset": offset,
                "limit": limit,
                "type": search_type,
                "version": self.api_version
            }
            return json
        elif search_type == "ALL":
            json = {
                "s": s,
                "type": search_type,
                "version": self.api_version
            }
            return json

    def search_in_chat_json(self, chat_hash: str, s: str, offset: int, limit: int):
        json = {
            "hash": chat_hash,
            "s": s,
            "offset": offset,
            "limit": limit,
            "version": self.api_version
        }
        return json