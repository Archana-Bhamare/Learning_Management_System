import datetime
import jwt
from LMSystem.settings import SECRET_KEY


def token_activation(username, password=None):
    data = {
        'username': username,
        'password': password,
        'exp': datetime.datetime.now() + datetime.timedelta(days=1)
    }

    token = jwt.encode(data, SECRET_KEY, algorithm="HS256").decode('utf-8')
    return token