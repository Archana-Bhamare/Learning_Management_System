from django.urls import path
from . import views

urlpatterns = [
    path('addcourse', views.AddCourseAPI.as_view(), name='addcourse'),
    path('updatecourse/<int:course_id>', views.UpdateCourseAPI.as_view(), name='updatecourse'),
    path('updatestudent/<int:student_id>', views.UpdateStudentDetailsAPI.as_view(), name='updatestudent'),
    path('updateeducation/', views.UpdateStudentEducationAPI.as_view(), name='updateeducation'),
    path('updatementor/<int:mentor_id>', views.UpdateMentorDetailsAPI.as_view(), name='updatementor'),
    path('displaymentor/', views.DisplayMentorDetailsAPI.as_view(), name='displyamentor'),
    path('studentmentor/', views.StudentMentorAPI.as_view(), name='studentmentor')
]
