import logging
import jwt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from Authentication.models import User
from Authentication.permissions import IsAdmin
from Authentication.serializer import UserSerializer, UserLoginSerializer, ChangeUserPasswordSerializer, \
    ResetPasswordSerializer, ForgotPasswordSerializer
from Authentication.mailconfigure import Email
from rest_framework_jwt.utils import jwt_payload_handler
from Learning_System import settings
from Learning_System.settings import file_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

class UserRegistrationAPI(GenericAPIView):
    """ This API is used to Register the User"""
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)

    def post(self, request):
        """
        This function is used to add User with role like Mentor, Engineer and Admin
        :param request:  User Data
        :return: Successful register the user
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        user_role = data['role']
        email = data['email']
        user = User.objects.get(email=email)
        user.set_password(data['password'])
        user.save()
        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY).decode('UTF-8')
        data = {
            'email': user.email,
            'reverse': 'login',
            'token': token,
            'message': "Hello " + user.get_full_name() + ',' + 'You are added as a new ' + user_role + '. \n' + 'Please Login with the following credentials' + "\nUsername - " + user.username + "\tPassword - " +
                       data['password'] + '\nThank You,' + '\nLearning Management System Team',
            'subject': 'You are Successfully Register',
            'site': get_current_site(request).domain
        }
        Email.email_validation(data)
        Email.send_email(Email.email_validation(data))
        logger.info({f'New {user_role} is added successfully'})
        return Response({f'New {user_role} is added successfully'}, status=status.HTTP_201_CREATED)


class UserLoginAPI(GenericAPIView):
    """ This API is used to logged in the user"""
    serializer_class = UserLoginSerializer

    def post(self, request):
        """
        This function used to logged in the user by username and password
        :param request: user data
        :return: user logged in
        """
        token = request.GET.get('token')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user = authenticate(username=user_data['username'], password=user_data['password'])
        if user:
            if token:
                if user.is_first_login:
                    token = request.GET.get('token')
                    jwt.decode(token, settings.SECRET_KEY)
                    login(request, user)
                    logger.info("User Login Successfully")
                    return redirect('changepassword')
            elif not token and not user.is_first_login:
                login(request, user)
                logger.info("You are Login successfully")
                return Response("You are Login successfully", status=status.HTTP_200_OK)
        logger.error("Invalid user")
        return Response("Invalid user", status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(login_required(login_url='/User/login/'), name='dispatch')
class UserLogoutAPI(GenericAPIView):
    """ This Logout API used to logout the user"""
    serializer_class = UserLoginSerializer

    def get(self, request):
        """
        This function used to logout the user
        @param request: User logout request
        @return: logout user
        """
        logout(request)
        logger.info("Successfully logged out")
        return Response("Successfully logged out", status=status.HTTP_200_OK)


class ChangeUserPasswordView(GenericAPIView):
    """ This API is used to change the user password"""
    serializer_class = ChangeUserPasswordSerializer

    def put(self, request):
        """
        This function used to change old password with new password
        :param request: old password
        :return: Change the old password with new password
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.data.get('new_password')
        confirm_password = serializer.data.get('confirm_password')
        if new_password != confirm_password:
            logger.error("New Password Mismatch")
            return Response("Password Mismatch", status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(raw_password=serializer.data.get('new_password'))
        request.user.is_first_login = False
        request.user.save()
        logger.info("Password changed successfully")
        return Response("Password changed successfully", status=status.HTTP_200_OK)


class ForgotPassword(GenericAPIView):
    """ This API is used to reset the forgot password"""
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        """This API is used to send reset password link to user email id
        :param request: user email id
        :return: password reset link with jwt token
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        try:
            user = User.objects.get(email=user_data['email'])
        except:
            return Response("Email Id not Valid", status=status.HTTP_404_NOT_FOUND)
        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY).decode('UTF-8')

        email_data = {
            'email': user.email,
            'reverse': 'resetpassword',
            'token': token,
            'message': "Hello " + user.get_full_name() + '!' + "\nYou recently requested to reset your password." + "\nClick on the following link to reset your password." + "\nThank You," + "\nLearning Management System Team",
            'subject': 'Forgotten password reset',
            'site': get_current_site(request).domain
        }
        Email.email_validation(email_data)
        Email.send_email(Email.email_validation(email_data))
        logger.info("Reset password link sent")
        return Response("Please check your email address to reset password", status=status.HTTP_200_OK)


class ResetPasswordAPI(GenericAPIView):
    """ This API used to reset the password"""
    serializer_class = ResetPasswordSerializer

    def put(self, request):
        """
        This function used to reset the user forgot password
        :param request: User password
        :return: successfully reset password
        """
        token = request.GET.get('token')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        password = serializer.data.get('password')
        confirm_password = serializer.data.get('confirm_password')
        if password != confirm_password:
            logger.error("Password Mismatch")
            return Response("Password Mismatch", status=status.HTTP_400_BAD_REQUEST)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            user.set_password(user_data['password'])
            user.save()
            logger.info("Successfully Reset Password")
            return Response("Successfully Reset Password", status=status.HTTP_200_OK)
        except jwt.exceptions.DecodeError:
            logger.error("Invalid Token")
            return Response("Invalid Token", status=status.HTTP_400_BAD_REQUEST)
