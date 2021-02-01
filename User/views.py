import logging
from django.contrib.auth import login, logout
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from LMSystem.settings import file_handler
from User.mailconfigure import Email
from User.models import User
from User.serializer import UserRegisterSerializer, UserLoginSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.hashers import make_password, check_password

from User.token import TokenAuthentication

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
            passwd = make_password(password)
            user = User.objects.create(first_name=first_name, last_name=last_name,
                                       username=username, email=email,
                                       password=passwd, mob_no=mob_no, role=role)
            user.save()
            try:
                if role == "Engineer" or role == "Mentor":
                    token = TokenAuthentication.token_activation(username=request.data['username'],
                                                                 password=request.data['password'])
                    data = {
                        'name': f"{request.data['first_name']} {request.data['last_name']}",
                        'username': request.data['username'],
                        'password': request.data['password'],
                        'role': request.data['role'],
                        'email': request.data['email'],
                        'site': get_current_site(request).domain,
                        'token': token
                    }
                    Email.sendEmail(Email.email_validation(data))
                    return Response({'response': f"A new {user.role} is added successfully"},
                                    status=status.HTTP_201_CREATED)
            except:
                logger.error("Something went Wrong")
                return Response("Something went wrong",
                                status=status.HTTP_400_BAD_REQUEST)
            logger.info("Admin Register Successfully")
            return Response("Admin Register Successfully", status=status.HTTP_200_OK)


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
        try:
            user = User.objects.get(username=username)
            password_match = check_password(password, user.password)
            if user and password_match:
                if user.first_login:
                    token = request.GET.get('token')
                    if TokenAuthentication.verifyToken(token):
                        login(request, user)
                        user.save()
                        return redirect('changepassword')
                elif not user.first_login:
                    login(request, user)
                    logger.info("You are logged in Successfully")
                return Response("You are logged in Successfully",
                                status=status.HTTP_200_OK)
        except User.DoesNotExist:
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


class ChangePasswordAPI(GenericAPIView):
    """ This API is used to change the user password"""
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        """
        This function used to change old password with new password
        :param request: old password
        :return: Change the old password with new password
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data.get('password')
        if check_password(password, request.user.password):
            request.user.set_password(serializer.data.get('new_password'))
            request.user.save()
            logger.info("Password Change Successfully")
            return Response("Password Change Successfully", status=status.HTTP_200_OK)
        logger.error("Password Mismatch")
        return Response("Password Mismatch", status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordAPI(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        """This API is used to send reset password link to user email id
        @param request: user email id
        @return: password reset link with jwt token
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.data.get('email'))
        except User.DoesNotExist:
            return Response("Email does not exist", status=status.HTTP_404_NOT_FOUND)
        email_data = {
            'user': user,
            'site': get_current_site(request).domain,
            'token': TokenAuthentication.token_activation(username=user.username, password=user.password)
        }
        Email.sendEmail(Email.reset_password(email_data))
        logger.info('Reset Password link sent')
        return Response("Please check your email address to reset password", status=status.HTTP_200_OK)

# class ResetPasswordAPI(GenericAPIView):
#     serializer_class = ResetPasswordSerializer
#     def post(self,request):
#         token = request.GET.get('token')
#         password = request.data['password']
#         confirm_password = request.data['confirm_password']
#         if password == "" or confirm_password == "":
#             logger.error("you can not put empty field")
#             return Response("you can not put empty field")
#         if password == confirm_password:
#             userdata = TokenAuthentication.verifyToken(token)
#             if userdata:
#                 user = userdata.get('username')
#                 user.set_password(password)
#                 user.save()
#                 logger.info("successful reset password")
#                 return Response("successful reset password")
#         else:
#             logger.error("Password Mismatch")
#             return Response("password mismatch")
