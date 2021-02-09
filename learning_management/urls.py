from django.urls import path
from . import views
from .views import PerformanceAPI

urlpatterns = [
    path('addcourse', views.AddCourseAPI.as_view(), name='addcourse'),
    path('update-course/<int:course_id>', views.UpdateCourseAPI.as_view(), name='update-course'),
    path('student-details/<int:student_id>', views.StudentDetailsAPI.as_view(), name='student-details'),
    path('update-student/<int:student_id>', views.UpdateStudentDetailsAPI.as_view(), name='update-student'),
    path('student-education/<int:student_id>', views.StudentEducationAPI.as_view(), name='student-education'),
    path('update-education/<int:student_id>', views.UpdateStudentEducationAPI.as_view(), name='update-education'),
    path('display-student/', views.DisplayStudentAPI.as_view(), name='display-student'),
    path('update-mentor/<int:mentor_id>', views.MentorDetailsAPI.as_view(), name='update-mentor'),
    path('display-mentor/', views.DisplayMentorDetailsAPI.as_view(), name='display-mentor'),
    path('student-mentor/', views.StudentMentorAPI.as_view(), name='student-mentor'),
    path('performance/<int:student_id>/', views.PerformanceAPI.as_view(), name='performance'),
]

