import requests

from BaseDirectory.BaseModule import main_api_url, main_headers, last_version, Base


class System(Base):
    @staticmethod
    def system_health_request():
        """Корректный запрос"""
        system_req = requests.get(f"{main_api_url}/health", headers=main_headers)
        assert system_req.status_code == 200
        assert system_req.json()["response"] == True
        """Неккоретный запрос(Без указания заголовков). Ответ должен быть 200-ым, так как авторизация тут не играет роли"""
        no_headers_req = requests.get(f"{main_api_url}/health")
        assert no_headers_req.status_code == 200
        assert no_headers_req.json()["response"] == True

    def system_last_version_request(self):
        """Корректный запрос"""
        last_version_req = requests.get(f"{self.main_api_url}/version", headers=main_headers)
        assert last_version_req.status_code == 200
        print(last_version_req.json()["response"])
        assert last_version_req.json()["response"]["current_version"] == self.last_version
        assert last_version_req.json()["response"]["latest_version"] == self.last_version
        """Неккоректный запрос(без указания заголовков). Ответ должен быть 200-ым, так как авторизация тут не играет роли"""
        no_headers_req = requests.get(f"{self.main_api_url}/version")
        assert no_headers_req.status_code == 200
        assert no_headers_req.json()["response"]["current_version"] == self.last_version
        assert no_headers_req.json()["response"]["latest_version"] == self.last_version
