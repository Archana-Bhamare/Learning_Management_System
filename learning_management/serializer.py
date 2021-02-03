from rest_framework import serializers
from .models import *


class AddCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name', 'description']


class UpdateStudentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['alternate_mobile_number', 'relation_with_alt_num', 'current_location', 'current_address', 'git_link',
                  'year_of_exp']

class UpdateStudentEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class UpdateMentorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['course']

class StudentMentorSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = StudentMentor
        fields = ['student','mentor']
