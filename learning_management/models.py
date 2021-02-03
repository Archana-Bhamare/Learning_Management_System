from django.db import models
from Authentication.models import User

class Course(models.Model):
    course_name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name

class Student(models.Model):
    student = models.OneToOneField(to=User, on_delete=models.CASCADE)
    alternate_mobile_number = models.CharField(max_length=13, default=None, null=True)
    relation_with_alt_num = models.CharField(max_length=30, default=None, null=True)
    current_location = models.CharField(max_length=50,default=None,null=True)
    current_address = models.CharField(max_length=100, default=None, null=True)
    git_link = models.CharField(max_length=60, default=None, null=True)
    year_of_exp = models.IntegerField(default=None,null=True)

    def __str__(self):
        return self.student.get_full_name()

class Education(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    university = models.CharField(max_length=30, default=None, null=True)
    degree = models.CharField(max_length=20,default=None,null=True)
    degree_stream = models.CharField(max_length=50,default=None,null=True)
    percentage = models.FloatField(default=None,null=True)
    from_date = models.DateField(default=None,null=True)
    till = models.DateField(default=None,null=True)

    def __str__(self):
        return self.student.student.get_full_name()

class Mentor(models.Model):
    mentor = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course)

    def __str__(self):
        return self.mentor.get_full_name()

class StudentMentor(models.Model):
    student =models.OneToOneField(Student, on_delete=models.CASCADE)
    mentor = models.OneToOneField(Mentor, on_delete=models.SET_NULL, null=True)
    course = models.OneToOneField(Course, on_delete=models.SET_NULL, null=True)

class Performance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    current_score = models.FloatField(default=None)

    def __str__(self):
        return self.student.student.get_full_name()
