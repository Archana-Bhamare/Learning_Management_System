from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegisterAPI.as_view(), name='register'),
    path('activate/<surl>/', views.activate, name="activate"),
]