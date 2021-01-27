from django.db import models

class User(models.Model):
    choices = (
        ('Mentor', 'Mentor'),
        ('Engineer', 'Engineer'),
        ('Admin', 'Admin'),
    )
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    mob_no = models.CharField(max_length=13, default=None)
    role = models.CharField(choices=choices, max_length=20)
