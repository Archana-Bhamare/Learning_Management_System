from django.db import models
from django.utils.timezone import now

class User(models.Model):
    choices = (
        ('Mentor', 'Mentor'),
        ('Engineer', 'Engineer'),
        ('Admin', 'Admin'),
    )
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    username = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=20, default=None, null=True)
    mob_no = models.CharField(max_length=13, default=None, null=True)
    role = models.CharField(choices=choices, max_length=20)
    last_login = models.DateTimeField(default=now)
    first_login = models.BooleanField(default=True)
