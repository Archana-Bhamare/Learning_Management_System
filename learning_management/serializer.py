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
        fields = ['id', 'alternate_mobile_number', 'relation_with_alt_num', 'current_location', 'current_address',
                  'git_link',
                  'year_of_exp']
        extra_kwargs = {'id': {'read_only': True}}


class UpdateStudentEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id','university','degree','degree_stream','percentage','from_date','till']
        extra_kwargs = {'id': {'read_only': True}}

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
    class Meta:
        model = StudentMentor
        fields = ['student', 'mentor', 'course']


class StudentMentorDetailSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StudentMentor
        fields = ['student', 'mentor', 'course']

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ['student', 'mentor', 'course', 'current_score']

class PerformanceDetailsSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Performance
        fields = '__all__'
