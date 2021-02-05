from django.dispatch import receiver
from django.db.models.signals import post_save
from Authentication.models import User
from learning_management.models import Student, Education, Mentor


@receiver(post_save, sender=User)
def create_student_details(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'Engineer':
            student = Student.objects.create(student=instance)
            Education.objects.create(student=student)
        elif instance.role == 'Mentor':
            Mentor.objects.create(mentor=instance)
