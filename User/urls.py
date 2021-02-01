from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegisterAPI.as_view(), name='register'),
    path('login/', views.UserLoginAPI.as_view(), name='login'),
    path('changepassword/', views.ChangePasswordAPI.as_view(), name='changepassword'),
    path('logout/', views.UserLogoutAPI.as_view(), name='logout'),
    path('forgotpassword/', views.ForgotPasswordAPI.as_view(), name='forgotpassword'),
    #path('resetpassword/', views.ResetPasswordAPI.as_view(), name='resetpassword'),
]