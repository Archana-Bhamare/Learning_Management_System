from django.urls import path
from . import views

urlpatterns = [
    path('addcourse', views.AddCourseAPI.as_view(), name='addcourse'),
    path('updatestudent', views.UpdateStudentDetailsAPI.as_view(), name='updatestudent'),
    path('updatementor', views.UpdateMentorDetailsAPI.as_view(), name='updatementor'),
    path('updateeducation', views.UpdateStudentEducationAPI.as_view(), name='updateeducation'),
]
