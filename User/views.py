import logging
import jwt
from django.db.models import Q
from django_short_url.models import ShortURL
from django_short_url.views import get_surl
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from LMSystem import settings
from LMSystem.settings import file_handler
from User.models import User
from User.serializer import UserRegisterSerializer
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


class UserRegisterAPI(GenericAPIView):
    """ This API is used to Register the User"""
    serializer_class = UserRegisterSerializer

    def post(self, request):
        """
        This function is used to add User with role like Mentor, Engineer and Admin
        :param request:  User Data
        :return: Successful register the user
        """
        data = request.data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        mob_no = data.get('mob_no')
        role = data.get('role')
        if password != confirm_password:
            logger.error("password mismatch")
            return Response("password mismatch ", status=status.HTTP_400_BAD_REQUEST)
        user_email = User.objects.filter(
            Q(email__iexact=email)
        )
        if user_email.exists():
            logger.error("Email id already exist")
            return Response("Email id already exist", status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email,
                                       password=password, mob_no=mob_no)
            try:
                if role == "Engineer":
                    user.is_active = False
                    user.save()
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    url = str(token)
                    surl = get_surl(url)
                    short_token = surl.split("/")
                    message = "You are register successfully"
                    mail_message = render_to_string('email_validation.html', {
                        'user': user,
                        'domain': get_current_site(request).domain,
                        'surl': short_token[2]
                    })
                    recipients_email = email
                    email = EmailMessage(message, mail_message, to=[recipients_email])
                    email.send()
                    logger.info("Mail Successfully send to the Engineer")
                    return Response('Mail Successfully send to the Engineer',
                                    status=status.HTTP_200_OK)
                if role == "Mentor":
                    user.save()
                    logger.info("Mentor Register Successfully")
                    return Response("Successfully register Mentor", status=status.HTTP_200_OK)
            except:
                logger.error("Something went Wrong")
                return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)
            logger.info("Admin Register Successfully")
            return Response("Admin Register Successfully", status=status.HTTP_200_OK)


def activate(request, surl):
    """
        @param request: once the account verification link is clicked by user this will take that request
        @return: it will redirect to login page
    """
    try:
        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)
        if user is not None:
            user.is_active = True
            user.save()
            logger.info("successfully activate your account")
            return Response("successfully activate your account")
        else:
            logger.error("User not valid")
            return Response("User not valid")
    except KeyError:
        logger.error("Key Error")
        return Response("Key Error")