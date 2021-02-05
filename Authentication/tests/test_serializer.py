from Authentication.models import User
from Authentication.serializer import UserSerializer, ForgotPasswordSerializer, UserLoginSerializer, \
    ChangeUserPasswordSerializer, ResetPasswordSerializer
from django.test import TestCase


class TestSerializer(TestCase):
    def setUp(self):
        """
        This is setup for testing serializers
        """
        # User Attributes
        self.user_attributes = {
            'username': 'Archana',
            'first_name': 'Archana',
            'last_name': 'Bhamare',
            'email': 'bhamarearchana2@gmail.com',
            'password': '12345',
            'mobile_number': '8529637410',
            'role': 'Engineer'
        }
        # User Login serializer attributes
        self.login_attributes = {
            'username': 'Archu',
            'password': '12345'
        }
        # User Forgot Password serializer attributes
        self.forgot_attributes = {
            'email': 'bhamarearchana2@gmail.com'
        }
        # User change password serializer attributes
        self.change_password_attributes = {
            'new_password': '12345',
            'confirm_password': '123456'
        }
        # User reset password serializer attributes
        self.reset_password_attributes = {
            'password': '12345',
            'confirm_password': '12345'
        }
        self.user = User.objects.create(**self.user_attributes)
        self.user_serializer = UserSerializer(instance=self.user)
        self.forgot_serializer = ForgotPasswordSerializer(instance=self.user)
        self.login_serializer = UserLoginSerializer(instance=self.login_attributes)
        self.change_password_serializer = ChangeUserPasswordSerializer(instance=self.change_password_attributes)
        self.reset_password_serializer = ResetPasswordSerializer(instance=self.user)

    # Test cases for user serializer
    def test_User_Serializers_Contains_Expected_Fields(self):
        """ This test case test the user serializer contains expected fields """
        data = self.user_serializer.data
        self.assertEqual(set(data.keys()),
                         {'username', 'first_name', 'last_name', 'email', 'password', 'mobile_number', 'role'})

    def test_User_Serializer_Username_Field(self):
        """ This test case test the user serializer fields"""
        data = self.user_serializer.data
        self.assertEqual(data['username'], self.user_attributes['username'])

    def test_User_Serializer_Username_Fields_Null_Content(self):
        """ This test case test the username field contains null content"""
        self.user_attributes['username'] = ''
        serializer = UserSerializer(data=self.user_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'username'})

    def test_User_Serializer_Username_Field_Valid_Content(self):
        """ This test case test the username field contains valid content"""
        self.user_attributes['username'] = 'Archu'
        serializer = UserSerializer(data=self.user_attributes)
        self.assertTrue(serializer.is_valid())

    # Test cases for forgot password serializer
    def test_Forgot_Password_Serializers_Fields(self):
        data = self.forgot_serializer.data
        self.assertEqual(set(data.keys()),
                         {'email'})

    def test_Forgot_Password_Serializer_Email_Field(self):
        data = self.forgot_serializer.data
        self.assertEqual(data['email'], self.forgot_attributes['email'])

    def test_Forgot_Password_Serializer_Email_Field_Invalid_Content(self):
        self.forgot_attributes['email'] = 'archu'
        serializer = ForgotPasswordSerializer(data=self.forgot_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'email'})

    def test_Forgot_Password_Serializer_Email_Field_Valid_Content(self):
        self.forgot_attributes['email'] = 'bhamarearchana@gmail.com'
        serializer = ForgotPasswordSerializer(data=self.forgot_attributes)
        self.assertTrue(serializer.is_valid())

    # test cases for login serializer
    def test_Login_Serializer_Contains_Expected_Fields(self):
        data = self.login_serializer.data
        self.assertEqual(set(data.keys()), {'username', 'password'})

    def test_Login_Serializer_Username_Field(self):
        data = self.login_serializer.data
        self.assertEqual(data['username'], self.login_attributes['username'])

    def test_Login_Serializer_Username_Fields_Content_Null(self):
        self.login_attributes['username'] = ''
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'username'})

    def test_Login_Serializer_Username_Fields_Content_Min_length(self):
        self.login_attributes['username'] = 'a'
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'username'})

    def test_Login_Serializer_Username_Fields_Content_Max_length(self):
        self.login_attributes['username'] = 'abhjkiolhjfdssfdgfdgttgthgth'
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'username'})

    def test_Login_Serializer_password_Fields_Content_Null(self):
        self.login_attributes['password'] = ''
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'password'})

    def test_Login_Serializer_Password_Fields_Content_Min_length(self):
        self.login_attributes['password'] = 'a'
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'password'})

    def test_Login_Serializer_Password_Fields_Content_Max_length(self):
        self.login_attributes['password'] = 'abhjkiolhjfdssasdfghjklou'
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'password'})

    def test_Login_Serializer_password_Fields_Valid_Content(self):
        self.login_attributes['password'] = '123456'
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertTrue(serializer.is_valid())

    def test_Login_Serializer_Username_Fields_Valid_Content(self):
        self.login_attributes['username'] = 'Archesh'
        serializer = UserLoginSerializer(data=self.login_attributes)
        self.assertTrue(serializer.is_valid())

    # test cases for change password serializer
    def test_Change_Password_Serializer_Contains_Expected_Fields(self):
        data = self.change_password_serializer.data
        self.assertEqual(set(data.keys()), {'new_password', 'confirm_password'})

    def test_Change_Password_Serializer_Username_Field(self):
        data = self.change_password_serializer.data
        self.assertEqual(data['new_password'], self.change_password_attributes['new_password'])

    def test_Change_Password_Serializer_Username_Fields_Content_Null(self):
        self.change_password_attributes['new_password'] = ''
        serializer = ChangeUserPasswordSerializer(data=self.change_password_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'new_password'})

    def test_Change_Password_Serializer_Username_Fields_Content_Min_length(self):
        self.change_password_attributes['new_password'] = 'a'
        serializer = ChangeUserPasswordSerializer(data=self.change_password_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'new_password'})

    def test_Change_Password_Serializer_Username_Fields_Content_Max_length(self):
        self.change_password_attributes['new_password'] = 'abhjkiolhjfdssdfgdg'
        serializer = ChangeUserPasswordSerializer(data=self.change_password_attributes)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), {'new_password'})

    def test_Change_Password_Serializer_Username_Fields_Valid_Content(self):
        self.change_password_attributes['new_password'] = '12345'
        serializer = ChangeUserPasswordSerializer(data=self.change_password_attributes)
        self.assertTrue(serializer.is_valid())
