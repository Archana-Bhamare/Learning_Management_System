import logging
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from LMSystem.settings import file_handler
from User.permissions import isAdmin
from User.serializer import UserRegisterSerializer

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
        email = data.get('email')
        role = data.get('role')
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        serializer.save()
        try:
            if role == "Engineer":
                message = "You are register successfully"
                mail_message = render_to_string('email_validation.html', {
                    'domain': get_current_site(request).domain,
                })
                recipients_email = email
                email = EmailMessage(message, mail_message, to=[recipients_email])
                email.send()
                logger.info("Mail Successfully send to the Engineer")
                return Response('Mail Successfully send to the Engineer',
                                status=status.HTTP_200_OK)
            if role == "Mentor":
                logger.info("Mentor Register Successfully")
                return Response("Successfully register Mentor", status=status.HTTP_200_OK)
        except:
            logger.error("Something went Wrong")
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)
        logger.info("Admin Register Successfully")
        return Response("Admin Register Successfully", status=status.HTTP_200_OK)
