class LinkJson:
    def add_link_json(self, url: str, name: str, version: str):
        link = {
            "url": url,
            "name": name,
            "version": version
        }
        return link
