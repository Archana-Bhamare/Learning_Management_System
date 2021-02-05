import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from Authentication.permissions import IsStudent, IsMentor, IsAdmin
from Learning_System.settings import file_handler
from learning_management.models import *
from learning_management.serializer import AddCourseSerializer, UpdateStudentDetailsSerializer, \
    UpdateMentorDetailsSerializer, UpdateStudentEducationSerializer, \
    DisplayMentorCourseSerializer, StudentMentorSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


class AddCourseAPI(GenericAPIView):
    """ This API used for adding Courses """
    serializer_class = AddCourseSerializer
    queryset = Course.objects.all()
    permission_classes = (IsAdmin,)

    def get(self, request):
        """
        This function used for getting all the course
        :param request: course
        :return: returned all the courses
        """
        try:
            course = Course.objects.all()
            serializer = self.serializer_class(course, many=True)
            logger.info("Display all the Course")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            logger.error("Something went wrong!!!")
            return Response("Something went wrong!!!", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        This function is used for adding the course
        :param request: course name and description
        :return: Add the courses
        """
        data = request.data
        serializer = self.serializer_class(data=data)
        try:
            serializer.is_valid()
            serializer.save()
            logger.info("New Course is Added")
            return Response("New Course is Added ", status=status.HTTP_201_CREATED)
        except Exception:
            logger.error("Something went wrong!!!")
            return Response("Something went wrong!!!", status=status.HTTP_403_FORBIDDEN)


class UpdateCourseAPI(GenericAPIView):
    """ This API is used for Update and Delete the course"""
    serializer_class = AddCourseSerializer
    queryset = Course.objects.all
    permission_classes = (IsAdmin,)

    def get(self, request, course_id):
        """
        This function is used for getting the course with particular id
        :param request: course
        :param course_id: course id
        :return: returned the course with particular id
        """
        try:
            course = Course.objects.get(pk=course_id)
            serializer = self.serializer_class(course)
            logger.info("Displaying the course")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.info("Course not found!!!")
            return Response("Course not found!!!", status=status.HTTP_404_NOT_FOUND)
        except Exception:
            logger.error("Something went wrong!!!")
            return Response("Something went wrong!!!", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, course_id):
        """
        This function is used for update the existing course
        :param request: course name and description
        :param course_id: course id
        :return: update the particular course
        """
        try:
            course = Course.objects.get(pk=course_id)
            serializer = self.serializer_class(course, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info("Course update successfully")
                return Response("Course update successfully", status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.error("Course not found!!!")
            return Response("Course not found!!!", status=status.HTTP_404_NOT_FOUND)
        except Exception:
            logger.error("Something went wrong!!!")
            return Response("Something went wrong!!!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, course_id):
        """
        This function is used for delete course with particular
        :param request: course id
        :param course_id: course id
        :return: Delete the course
        """
        try:
            course = Course.objects.get(pk=course_id)
            course.delete()
            logger.info("Course deleted successfully")
            return Response("Course deleted successfully", status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.error("Course not found!!!")
            return Response("Course not found!!!", status=status.HTTP_404_NOT_FOUND)
        except Exception:
            logger.error("Something went wrong!!!")
            return Response("Something went wrong!!!", status=status.HTTP_403_FORBIDDEN)


class UpdateStudentDetailsAPI(GenericAPIView):
    """ This API is used for updating the student personal details"""
    serializer_class = UpdateStudentDetailsSerializer
    queryset = Student.objects.all()
    permission_classes = (IsStudent,)

    def get(self, request, student_id):
        """
        This function is used for getting the student with particular student id
        :param request: student id
        :param student_id: student id
        :return: returned the student data
        """
        try:
            student = Student.objects.filter(pk=student_id)
            if student:
                serializer = self.serializer_class(student, many=True)
                logger.info("Display student data")
                return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.error("Student not found!!!")
            return Response("Student Not found!!!", status=status.HTTP_404_NOT_FOUND)
        except Exception:
            logger.error("Something went wrong!!!")
            return Response("Something went wrong!!!", status=status.HTTP_403_FORBIDDEN)

    def put(self, request, student_id):
        """
        This function is used for updating the student data
        :param request: student personal details
        :param student_id: student id
        :return: update the student data
        """
        try:
            student = Student.objects.get(pk=student_id)
            serializer = self.serializer_class(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info("Student details updated")
            return Response("Student details Updated", status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.error("Student not found!!!")
            return Response("Student not found!!!", status=status.HTTP_404_NOT_FOUND)
        except Exception:
            logger.error("Something went wrong!!!")
            return Response("Something went wrong!!!", status=status.HTTP_403_FORBIDDEN)


class UpdateStudentEducationAPI(GenericAPIView):
    """ This API is used to update the student education details"""
    serializer_class = UpdateStudentEducationSerializer
    queryset = Education.objects.all()
    permission_classes = (IsStudent,)

    def get(self, request):
        """
        This function is used to getting student educational details
        :param request: student educational details
        :return: returned the student data
        """
        try:
            student = Education.objects.filter(student=self.request.user.student)
            serializer = self.serializer_class(student, many=True)
            logger.info("Display student data")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.error("student not found!!!")
            return Response("Student not found!!!", status=status.HTTP_404_NOT_FOUND)
        except Exception:
            logger.error("Something went wrong!!!")
            return Response("Something went wrong!!!", status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        """
        This function is used for updating the student educational details
        :param request: student personal details
        :return: update the student educational details
        """
        try:
            student = Education.objects.get(student=self.request.user.student)
            serializer = self.serializer_class(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info("Student education details updated")
            return Response("Student education details Updated", status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.error("Student not found!!!")
            return Response("Student Not Found!!!", status=status.HTTP_404_NOT_FOUND)
        except Exception:
            logger.error("Something went wrong!!!")
            return Response("Something went wrong!!!", status=status.HTTP_403_FORBIDDEN)


class UpdateMentorDetailsAPI(GenericAPIView):
    """ This API used for update the Mentor details"""
    serializer_class = UpdateMentorDetailsSerializer
    queryset = Mentor.objects.all()
    permission_classes = (IsMentor,)

    def get(self, request, mentor_id):
        """
        This function is used to getting the mentor with particular mentor id
        :param request: mentor's id
        :param mentor_id: mentor's id
        :return: returned the mentor data
        """
        try:
            mentor = Mentor.objects.filter(pk=mentor_id)
            if mentor:
                serializer = DisplayMentorCourseSerializer(mentor, many=True)
                logger.info("Display mentor data")
                return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.error("Mentor not found!!!")
            return Response("Mentor not found!!!", status=status.HTTP_404_NOT_FOUND)
        except Exception:
            logger.error("Something went wrong!!!")
            return Response("Something went wrong!!!", status=status.HTTP_403_FORBIDDEN)

    def put(self, request, mentor_id):
        """
        This function is used to update the mentor data
        :param request: mentor and course
        :param mentor_id: mentor's id
        :return: update the mentor data
        """
        try:
            mentor = Mentor.objects.get(pk=mentor_id)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            courses = serializer.validated_data['course']
            for course_name in courses:
                course = Course.objects.get(course_name=course_name)
                mentor.course.add(course.id)
                mentor.save()
            logger.info("Course added successfully...")
            return Response("Course added successFully...", status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.error("Mentor not found!!!")
            return Response("Mentor not found!!!", status=status.HTTP_404_NOT_FOUND)
        except Exception:
            logger.error("Something went wrong!!!")
            return Response("Something went wrong!!!", status=status.HTTP_403_FORBIDDEN)


class DisplayMentorDetailsAPI(GenericAPIView):
    """ This API used for displaying all the Mentor with associate course"""
    serializer_class = DisplayMentorCourseSerializer
    queryset = Mentor.objects.all()
    permission_classes = (IsAdmin,)

    def get(self, request):
        """
        This function is used for getting all the Mentors data with associate course
        :param request: mentor data
        :return: returned the mentor data with associate course
        """
        try:
            mentor = Mentor.objects.all()
            serializer = self.serializer_class(mentor, many=True)
            logger.info("Display Mentors list")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            logger.error("Something went wrong!!!")
            return Response("Something went wrong!!!", status=status.HTTP_403_FORBIDDEN)


class StudentMentorAPI(GenericAPIView):
    """ This API is used for assigning mentor and course to student"""
    serializer_class = StudentMentorSerializer
    queryset = StudentMentor.objects.all()

    def get(self, request):
        """
        This function is used for fetching all the students data
        @param request: Student data
        @return:  fetch all the student, mentor, course data
        """
        try:
            data = StudentMentor.objects.all()
            serializer = self.serializer_class(data, many=True)
            logger.info("Display student data")
            return Response(serializer.data)
        except Exception:
            logger.error("Something went wrong")
            return Response("Something went wrong", status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        """
        This function is used for assigning mentor and course to student
        :param request: student, mentor, course
        :return: assign mentor to student
        """
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            courses = serializer.validated_data['course']
            mentor = Mentor.objects.get()
            try:
                if courses in mentor.course.all():
                    serializer.save()
                    logger.info("Mentor assigned")
                    return Response("Mentor assigned", status=status.HTTP_200_OK)
            except Exception:
                logger.error("Mentor is not assigned for this course")
                return Response("Mentor is not assigned for this course", status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logger.error("Something went wrong")
            return Response("Something went wrong", status=status.HTTP_403_FORBIDDEN)
