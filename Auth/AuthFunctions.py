
import random
import string



def generate_random_domain():
    count = 13
    result = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=count)))
    return result

random_domain_name = generate_random_domain()
uncorrect_domain_name = "&&*&*^)("


fake_headers = {'token': 'Authorization', 'hash': 'Authorization-hash'}









