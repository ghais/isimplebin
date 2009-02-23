import random
from datetime import datetime

URL_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def make_token():
    random.seed()
    token = "".join(random.sample(URL_CHARS, 10))
    return token
