from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    role = (
        ('Engineer', 'Engineer'),
        ('Mentor', 'Mentor'),
        ('Admin', 'Admin')
    )
    mobile_number = models.CharField(max_length=13)
    role = models.CharField(choices=role, max_length=10)
    is_first_login = models.BooleanField(default=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
