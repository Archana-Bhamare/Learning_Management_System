from rest_framework import serializers
from .models import *


class AddCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'description']
        extra_kwargs = {'id': {'read_only': True}}

class UpdateStudentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id','alternate_mobile_number', 'relation_with_alt_num', 'current_location', 'current_address', 'git_link',
                  'year_of_exp']
        extra_kwargs = {'id': {'read_only': True}}

class UpdateStudentEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class UpdateMentorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['mentor', 'course']
        extra_kwargs = {'mentor': {'read_only': True}}

class DisplayMentorCourseSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True, many=True)
    class Meta:
        model = Mentor
        fields = ['mentor', 'course']

class StudentMentorSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StudentMentor
        fields = ['student', 'mentor']
