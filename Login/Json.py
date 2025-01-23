from BaseDirectory.BaseModule import Base, api_version


class LoginJson(Base):
    def geo_json(self, user_ip):
        json = {
            "ip": user_ip,
            "version": self.api_version
        }
        return json

    def json_for_refresh_jwt(self, refresh_param: (str, None)):
        json = {
            "refresh": refresh_param,
            "version": self.api_version
        }
        return json

    def json_for_create_registration_hash(self, company: bool):
        json = {
            "individual": company,
            "version": self.api_version
        }
        return json

    def json_for_domain_availability(self, registration_hash: (None, str), domain: (str, None)):
        json = {
            "hash_registration": registration_hash,
            "domain": domain,
            "version": self.api_version
        }
        return json

    def json_for_email_availability(self, registration_hash: (None, str), email: (str, None)):
        json = {
            "hash_registration": registration_hash,
            "email": email,
            "version": self.api_version
        }
        return json

    def json_for_login_other(self, user_id : (int, None)):
        json = {
            "user_id": user_id,
            "version": self.api_version
        }
        return json
    def json_for_get_code(self, phone: (None, int), email: (None, str)):
        json = {
            "phone": phone,
            "email": email,
            "version": self.api_version
        }
        return json

    def json_for_verification_code(self, phone: (None, int), email: (None, str), code: (None, int), hash_invite: (None, str)):
        if type(hash_invite) == str:
            json = {
                "phone": phone,
                "email": email,
                "code": code,
                "hash_invite": hash_invite,
                "version": self.api_version

            }
            return json
        else:
            json = {
                "phone": phone,
                "email": email,
                "code": code,
                "version": self.api_version

            }
            return json


