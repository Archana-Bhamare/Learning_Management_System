import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from Authentication.models import User


class TestUserViews(TestCase):

    def setUp(self):
        """
        This setup is for testing the views
        """
        self.client = Client()
        User.objects.create_user(username='Golu', email='archus@gmail.com',
                                 password='12345', role='Admin', is_first_login=False)
        User.objects.create_user(username='user', password='12345',
                                 email='bhamarearchana2@gmail.com')
        self.admin_login = {
            'username': 'Golu',
            'password': '12345'
        }
        self.user_valid_payload = {
            'username': 'Archesh',
            'first_name': 'Archesh',
            'last_name': 'Bhamare',
            'email': 'archanabhamare1997@gmail.com',
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
        self.forgot_valid_credentials = {
            'email': 'bhamarearchana2@gmail.com'
        }

    # Test cases for register user
    def test_Register_User_With_Valid_Payload(self):
        self.client.post(reverse('login'), data=json.dumps(self.admin_login), content_type='application/json')
        response = self.client.post(reverse('register'), data=json.dumps(self.user_valid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_Register_User_With_Invalid_Payload(self):
        self.client.post(reverse('login'), data=json.dumps(self.admin_login), content_type='application/json')
        response = self.client.post(reverse('register'), data=json.dumps(self.user_invalid_payload),
                                    content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test cases for login user
    def test_Login_User_With_Valid_Credentials_Without_Token(self):
        response = self.client.post(reverse('login'), data=json.dumps(self.user_valid_credentials),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_Login_User_With_Invalid_Credentials_Without_Token(self):
        response = self.client.post(reverse('login'), data=json.dumps(self.user_invalid_credentials),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_Login_User_With_Valid_Credentials_With_Token(self):
        self.client.post(reverse('login'), data=json.dumps(self.admin_login), content_type='application/json')
        response = self.client.post(reverse('register'), data=json.dumps(self.user_valid_payload),
                                    content_type='application/json')
        token = response.data['token']
        data = {
            'username': response.data['username'],
            'password': response.data['password']
        }
        respon = self.client.post('/User/login/?token=' + token, data=json.dumps(data),
                                  content_type='application/json')
        self.assertEqual(respon.status_code, status.HTTP_200_OK)

    def test_Login_User_With_Invalid_Credentials_With_Token(self):
        self.client.post(reverse('login'), data=json.dumps(self.admin_login), content_type='application/json')
        response = self.client.post(reverse('register'), data=json.dumps(self.user_valid_payload),
                                    content_type='application/json')
        token = response.data['token']
        data = {
            'username': 'Archu',
            'password': '45632'
        }
        respon = self.client.post('/User/login/?token=' + token, data=json.dumps(data),
                                  content_type='application/json')
        self.assertEqual(respon.status_code, status.HTTP_401_UNAUTHORIZED)

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

    #Test cases for Change Password
    def test_Change_Password_After_User_Login_With_Valid_Credentials(self):
        self.test_Login_User_With_Valid_Credentials_With_Token()
        data = {
            'new_password': '123456',
            'confirm_password': '123456'
        }
        response = self.client.put(reverse('changepassword'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Change_Password_After_User_Login_With_Invalid_Credentials(self):
        self.test_Login_User_With_Invalid_Credentials_With_Token()
        data = {
            'new_password': '123456',
            'confirm_password': '123456'
        }
        response = self.client.put(reverse('changepassword'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testcase for Forgot Password API
    def test_Forgot_Password_With_Invalid_User_Email(self):
        response = self.client.post(reverse('forgotpassword'), data=json.dumps({'email': 'archna@gmail.com'}),
                                    content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_Forgot_Password_With_Valid_User_Email(self):
        response = self.client.post(reverse('forgotpassword'), data=json.dumps(self.forgot_valid_credentials),
                                    content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    # Testcase for change password API
    def test_Reset_Password_With_Invalid_Token(self):
        self.test_Forgot_Password_With_Valid_User_Email()
        data = json.dumps({
            "password": "12345",
            "confirm_password": "123456"
        })
        response = self.client.put(
            '/User/resetpassword/?token=eyJ0eXAiOiJKV1QiLCJhbGciO2133219.eyJ1c2VyX2lkIjoyOSwidXNlcm5hbWUiOiJTdXNoIiwiZXhwIjoxNjEyMzI5NDUxLCJlbWFpbCI6ImJoYW1hcmVhcmNoYW5hQGdtYWlsLmNvbSJ9.zD7wUnwpN28WHVQqULYdk-lvZAnsy894U82tGa7b0yI',
            data=data, content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
