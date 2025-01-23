import random
import string
from random import randint


def generate_random_title_name():
    count = 15
    result = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=count)))
    return result


def generate_random_sort_param():
    count = random.randint(100, 1000)
    return count

print(generate_random_sort_param())