from django.core.mail import EmailMessage
from django.urls import reverse


class Email:
    @staticmethod
    def email_validation(data):
        link = 'http://' + data['site'] + reverse(data['reverse']) + "?token=" + str(data['token'])
        email_body = data['message'] + '\n' + link
        email_subject = data['subject']
        email_data = {'email_body': email_body, 'to_email': data['email'], 'email_subject': email_subject}
        return email_data

    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()
