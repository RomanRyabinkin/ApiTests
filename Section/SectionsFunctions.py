import random
import string

def random_string(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def random_number(first_number, second_number):
    number = random.randint(first_number, second_number)
    return number

