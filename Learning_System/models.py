from django.db import models
from User.models import User

class Course(models.Model):
    course_name = models.CharField(max_length=15)
    Description = models.CharField(max_length=50)

class Student(models.Model):
    yr_of_exp = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    alt_mob_no = models.CharField(max_length=13, default=None)
    rel_alt_no = models.CharField(max_length=10, default=None)
    current_location = models.CharField(max_length=20, default=None)
    current_address = models.CharField(max_length=25, default=None)
    git_link = models.CharField(max_length=50, default=None)
    year_of_exp = models.IntegerField(choices=yr_of_exp, default=None)

class Education(models.Model):
    student = models.OneToOneField(to=Student, on_delete=models.CASCADE)
    degree = models.CharField(max_length=50, default=None)
    stream = models.CharField(max_length=50, default=None)
    university = models.CharField(max_length=50, default=None)
    percentage = models.FloatField(default=None)
    from_date = models.DateField(default=None)
    till = models.DateField(default=None)

class Mentor(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(to=Course)

class Performance(models.Model):
    student = models.OneToOneField(to=Student, on_delete=models.CASCADE)
    mentor = models.OneToOneField(to=Mentor, on_delete=models.SET_NULL, null=True)
    course = models.OneToOneField(to=Course, on_delete=models.CASCADE)
    current_score = models.FloatField(default=None)
