import uuid
from random import randint


class GenerateEmail:
    def generate_email(self, string_length=15):
        """Returns a random string of length string_length."""
        random = str(uuid.uuid4())
        random = random.upper()
        random = random.replace("-", "")
        return f"{random[0:string_length]}@example.com"

    def random_with_N_digits(self, n):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    def get_phone(self):
        for mciNumbers in range(0, 100):
            # print(f'89{self.random_with_N_digits(9)}')
            return f'89{self.random_with_N_digits(9)}'

print(GenerateEmail.get_phone(self=GenerateEmail()))