from django.core.mail import EmailMessage
from django.urls import reverse


class Email:
    @staticmethod
    def email_validation(data):
        url = "http://" + data['site'] + reverse('login') + '?token=' + data['token']
        email_body = f"Hello {data['name']}, You are added as a new {data['role']} " \
                     f"\n Please login with the following credential \n" \
                     f" Username: {data['username']}, password: {data['password']} \n" \
                     f"\n Click Here - \n" \
                     f"Link: {url}"
        email_data = {'email_body': email_body, 'email_subject': 'You are register successfully', 'to_email': data['email']}
        return email_data

    @staticmethod
    def reset_password(data):
        url = "http://" + data['site'] + reverse('resetpassword', args=[data['token']])
        email_body = f"Hello {data['user'].first_name}, You recently requested to reset your password \n" \
                     f" Click on the following link to reset your password. \n" \
                     f"Link: {url}"
        email_data = {'email_body': email_body, 'email_subject': 'Forgotten password reset', 'to_email': data['user'].email}
        return email_data

    @staticmethod
    def sendEmail(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=(data['to_email'],)
        )
        email.send()
