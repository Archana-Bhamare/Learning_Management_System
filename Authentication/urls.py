from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationAPI.as_view(), name='register'),
    path('login/', views.UserLoginAPI.as_view(), name='login'),
    path('logout/', views.UserLogoutAPI.as_view(), name='logout'),
    path('changepassword/', views.ChangeUserPasswordView.as_view(), name='changepassword'),
    path('forgotpassword/', views.ForgotPassword.as_view(), name='forgotpassword'),
    path('resetpassword/',views.ResetPasswordAPI.as_view(), name='resetpassword'),
]
