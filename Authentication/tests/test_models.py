from django.test import TestCase
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
