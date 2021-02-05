from django.urls import path
from . import views

urlpatterns = [
    path('addcourse', views.AddCourseAPI.as_view(), name='addcourse'),
    path('update-course/<int:course_id>', views.UpdateCourseAPI.as_view(),name='update-course'),
    path('update-student/<int:student_id>', views.UpdateStudentDetailsAPI.as_view(), name='update-student'),
    path('update-education/',views.UpdateStudentEducationAPI.as_view(), name='update-education'),
    path('update-mentor/<int:mentor_id>', views.UpdateMentorDetailsAPI.as_view(), name='update-mentor'),
    path('display-mentor/',views.DisplayMentorDetailsAPI.as_view(),name='display-mentor'),
    path('student-mentor/', views.StudentMentorAPI.as_view(), name='student-mentor'),
    path('performance/', views.PerformanceAPI.as_view(), name='performance')
]
