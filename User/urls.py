from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegisterAPI.as_view(), name='register'),
    path('activate/<surl>/', views.activate, name="activate"),
    path('login/', views.UserLoginAPI.as_view(), name='login'),
    path('logout/', views.UserLogoutAPI.as_view(), name='logout'),
    path('forgotpassword/', views.ForgotPasswordAPI.as_view(), name='forgotpassword'),
]