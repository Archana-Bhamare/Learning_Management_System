import datetime
import jwt
from rest_framework.response import Response
from LMSystem.settings import SECRET_KEY


class TokenAuthentication:
    @staticmethod
    def token_activation(username, password):
        pay_load = {
            'username': username,
            'password': password,
            'exp': datetime.datetime.now() + datetime.timedelta(days=1)
        }
        token = jwt.encode(pay_load, SECRET_KEY)
        return token

    @staticmethod
    def verifyToken(token, secretkey=SECRET_KEY):
        try:
            verificationStatus = jwt.decode(token, key=secretkey, algorithms='HS256')
            return verificationStatus
        except jwt.ExpiredSignature:
            return Response("Token Expired")
