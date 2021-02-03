from django.contrib import admin
from .models import Performance, Course, Student, Education, Mentor, StudentMentor

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Education)
admin.site.register(Mentor)
admin.site.register(StudentMentor)
admin.site.register(Performance)
