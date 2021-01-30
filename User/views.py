import logging
import jwt
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import redirect
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
from User.serializer import UserRegisterSerializer, UserLoginSerializer, \
    ForgotPasswordFormSerializer
from rest_framework_jwt.settings import api_settings

from User.token import token_activation

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
            return Response("password mismatch ",
                            status=status.HTTP_400_BAD_REQUEST)
        user_email = User.objects.filter(
            Q(email__iexact=email)
        )
        if user_email.exists():
            logger.error("Email id already exist")
            return Response("Email id already exist",
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create(first_name=first_name, last_name=last_name,
                                       username=username, email=email,
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
                    return Response("Successfully register Mentor",
                                    status=status.HTTP_200_OK)
            except:
                logger.error("Something went Wrong")
                return Response("Something went wrong",
                                status=status.HTTP_400_BAD_REQUEST)
            logger.info("Admin Register Successfully")
            return Response("Admin Register Successfully", status=status.HTTP_200_OK)


def activate(request, surl):
    """
        @param request: once the account verification link is clicked by user this will
take that request
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
            return redirect('login')
        else:
            logger.error("User not valid")
            return redirect('login')
    except KeyError:
        logger.error("Key Error")
        return Response("Key Error")


class UserLoginAPI(GenericAPIView):
    """ This API is used to logged in the user"""
    serializer_class = UserLoginSerializer

    def post(self, request):
        """
        This function used to logged in the user by username and password
        :param request: user data
        :return: user logged in
        """
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            logger.info("You are logged in Successfully")
            return Response("You are logged in Successfully",
                            status=status.HTTP_200_OK)
        logger.error("Invalid User")
        return Response("Invalid User", status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutAPI(GenericAPIView):
    """ This Logout API used to logout the user"""
    serializer_class = UserLoginSerializer

    def get(self, request):
        """
        This function used to logout the user
        @param request: User logout request
        @return: logout user
        """
        try:
            logout(request)
            logger.info("Your Successfully Logged out")
            return Response("Your Successfully Logged out", status=status.HTTP_200_OK)
        except Exception:
            logger.error("Something Went Wrong")
            return Response("Something Went Wrong",
                            status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPI(GenericAPIView):
    """ This API is used for when user forgot password"""
    serializer_class = ForgotPasswordFormSerializer

    def post(self, request):
        """
        If user forgot his password then he can reset his password here
        @param request: user request
        @return: reset password
        """
        email = request.data['email']
        try:
            user = User.objects.filter(email=email)
            if user.count() == 0:
                logger.error("Not Found mail in database")
                return Response("Not Found mail in database")
            else:
                username = user.values()[0]["username"]
                current_site = get_current_site(request)
                domain_name = current_site.domain
                token = token_activation(username=username)
                url = str(token)
                surl = get_surl(url)
                short_token = surl.split('/')
                mail_subject = " Forgotten Password reset"
                msg = render_to_string('reset_email.html', {
                    'user': user,
                    'domain': domain_name,
                    'surl': short_token[2]
                })
                recipients = email
                email = EmailMessage(mail_subject, msg, to=[recipients])
                email.send()
                logger.info('Reset Password link sent')
                return Response('Please check your email address to reset password')
        except KeyError:
            logger.error("Key Error")
            return Response("Key error")
