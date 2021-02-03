import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from Authentication.models import User


class UserTest(TestCase):
    """ Test Models"""

    def setUp(self):
        User.objects.create(username='Archesh', first_name='Archesh', last_name='Bhamare',
                            email='archus@gmail.com', password='12345', mobile_number='8529637410',
                            role='Engineer')

    def test_User_username(self):
        user = User.objects.get(username='Archesh')
        self.assertEqual(user.username, 'Archesh')

    def test_User_EMail(self):
        user = User.objects.get(username='Archesh')
        self.assertEqual(user.email, 'archus@gmail.com')

    def test_User_Password(self):
        user = User.objects.get(username='Archesh')
        self.assertEqual(user.password, '12345')

    def test_User_Role(self):
        user = User.objects.get(username='Archesh')
        self.assertEqual(user.role, 'Engineer')

    def test_User_Invalid_Username(self):
        user = User.objects.get(username='Archesh')
        self.assertNotEqual(user.username, 'Archu')

    def test_User_Invalid_EMail(self):
        user = User.objects.get(username='Archesh')
        self.assertNotEqual(user.email, 'aarchus@gmail.com')

    def test_User_Invalid_Password(self):
        user = User.objects.get(username='Archesh')
        self.assertNotEqual(user.password, '123456')

    def test_User_Invalid_Role(self):
        user = User.objects.get(username='Archesh')
        self.assertNotEqual(user.role, 'Mentor')


class TestUserViews(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='Golu', email='archus@gmail.com',
                                 password='12345', role='Admin', is_first_login=False)

        self.admin_login = {
            'username': 'Golu',
            'password': '12345'
        }
        self.user_valid_payload = {
            'username': 'Archesh',
            'first_name': 'Archesh',
            'last_name': 'Bhamare',
            'email': 'bhamare2@gmail.com',
            'password': '12345',
            'mobile_number': '8529637410',
            'role': 'Mentor'
        }

        self.user_invalid_payload = {
            'username': 'Archu',
            'first_name': 'Archu',
            'last_name': '',
            'email': '',
            'password': '',
            'mobile_number': '8529637410',
            'role': 'Engineer'
        }
        self.user_valid_credentials = {
            'username': 'Archesh',
            'password': '12345'
        }
        self.user_invalid_credentials = {
            'username': 'Archesh',
            'password': ''
        }
        self.user_credentials = {
            'username': 'Darpan',
            'password': '123456'
        }

    # Test cases for register user
    def test_Register_User_With_Valid__Payload(self):
        self.client.post(reverse('login'), data=json.dumps(self.admin_login), content_type='application/json')
        response = self.client.post(reverse('register'), data=json.dumps(self.user_valid_payload),
                                    content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_Register_User_With_Invalid_Payload(self):
        self.client.post(reverse('login'), data=json.dumps(self.admin_login), content_type='application/json')
        response = self.client.post(reverse('register'), data=json.dumps(self.user_invalid_payload),
                                    content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test cases for login user
    def test_Login_User_With_Valid_Credentials(self):
        response = self.client.post(reverse('login'), data=json.dumps(self.user_valid_credentials),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Login_User_With_Invalid_Credentials(self):
        response = self.client.post(reverse('login'), data=json.dumps(self.user_invalid_credentials),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test cases for logout User API
    def test_Logout_User_With_Valid_Credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.user_valid_credentials),
                         content_type='application/json')
        response = self.client.get(reverse('logout'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_Logout_User_With_Invalid_Credentials(self):
        self.client.post(reverse('login'), data=json.dumps(self.user_invalid_credentials),
                         content_type='application/json')
        response = self.client.get(reverse('logout'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_Logout_User_without_Login(self):
        response = self.client.get(reverse('logout'), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    # Testcase for Forgot Password API
    def test_Forgot_Password_With_Valid_User_Login(self):
        self.test_Register_User_With_Valid__Payload()
        response = self.client.post(reverse('forgotpassword'), data=json.dumps({'email': 'bhamare@gmail.com'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testcase for change password API
    def test_Reset_Password_API_With_Invalid_Token(self):
        self.client.post(reverse('login'), data=json.dumps(self.admin_login), content_type='application/json')
        self.client.post(reverse('forgotpassword'),
                               data=json.dumps({'email': 'archus@gmail.com'}),
                               content_type='application/json')
        data = json.dumps({
            "password": "12345",
            "confirm_password": "123456"
        })
        response = self.client.put(
            '/User/resetpassword/?token=eyJ0eXAiOiJKV1QiLCJhbGciO2133219.eyJ1c2VyX2lkIjoyOSwidXNlcm5hbWUiOiJTdXNoIiwiZXhwIjoxNjEyMzI5NDUxLCJlbWFpbCI6ImJoYW1hcmVhcmNoYW5hQGdtYWlsLmNvbSJ9.zD7wUnwpN28WHVQqULYdk-lvZAnsy894U82tGa7b0yI',
            data=data, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
