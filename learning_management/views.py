import logging
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from Authentication.permissions import IsStudent, IsMentor, IsAdmin
from Learning_System.settings import file_handler
from learning_management.models import *
from learning_management.serializer import AddCourseSerializer, UpdateStudentDetailsSerializer, \
    UpdateMentorDetailsSerializer, UpdateStudentEducationSerializer, \
    DisplayMentorCourseSerializer

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
        course = Course.objects.all()
        serializer = self.serializer_class(course, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        This function is used for adding the course
        :param request: course name and description
        :return: Add the courses
        """
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info("New Course is Added")
        return Response("New Course is Added ", status=status.HTTP_201_CREATED)


class UpdateCourseAPI(GenericAPIView):
    """ This API is used for Update and Delete the course"""
    serializer_class = AddCourseSerializer
    queryset = Course.objects.all
    permission_classes = (IsAdmin,)

    def get(self, request, course_id):
        """
        This function is used for getting the course with particular id
        :param request: course id
        :return: returned the course with particular id
        """
        try:
            course = Course.objects.get(pk=course_id)
            serializer = self.serializer_class(course)
            logger.info("Displaying the course")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            logger.info("Course Not Found")
            return Response("Course not found", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, course_id):
        """
        This function is used for update the existing course
        :param request: course id
        :return: update the particular course
        """
        try:
            course = Course.objects.get(pk=course_id)
        except:
            logger.error("Course not found")
            return Response("Course not Found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Course Updated")
            return Response("Course updated", status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, course_id):
        """
        This function is used for delete course with particular
        :param request: course id
        :return: Delete the course
        """
        try:
            course = Course.objects.get(pk=course_id)
            course.delete()
            logger.info("Course Deleted")
            return Response("Course Deleted!!!", status=status.HTTP_200_OK)
        except:
            logger.error("Course not found")
            return Response("Course not Found", status=status.HTTP_404_NOT_FOUND)

class UpdateStudentDetailsAPI(GenericAPIView):
    """ This API is used for updating the student personal details"""
    serializer_class = UpdateStudentDetailsSerializer
    queryset = Student.objects.all()
    permission_classes = (IsStudent,)

    def get(self, request, student_id):
        """
        This function is used for getting the student with particular student id
        :param request: student id
        :return: returned the student data
        """
        student = Student.objects.filter(pk=student_id)
        if student:
            serializer = self.serializer_class(student, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error("Student not found")
        return Response("Student Not Found", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, student_id):
        """
        This function is used for updating the student data
        :param request: student id
        :return: update the student data
        """
        try:
            student = Student.objects.get(pk=student_id)
        except:
            logger.error("Student not found")
            return Response("Student Not Found",status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(student, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info("Student details updated")
        return Response("Student details Updated", status=status.HTTP_200_OK)

class UpdateStudentEducationAPI(GenericAPIView):
    """ This API is used to update the student education details"""
    serializer_class = UpdateStudentEducationSerializer
    queryset = Student.objects.all()
    permission_classes = (IsStudent,)

    def get(self, request, student_id):
        """
        This function is used to getting student educational details
        :param request: student id
        :return: returned the student data
        """
        student = Student.objects.filter(pk=student_id)
        if student:
            serializer = self.serializer_class(student, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error("student not found")
        return Response("Student Not Found", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, student_id):
        """
        This function is used for updating the student educational details
        :param request: student id
        :return: update the student educational details
        """
        try:
            student = Student.objects.get(pk=student_id)
        except:
            logger.error("Student not found")
            return Response("Student Not Found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(student, data=request.data)
        serializer.is_valid(raise_exception=True)


class UpdateMentorDetailsAPI(GenericAPIView):
    """ This API used for update the Mentor details"""
    serializer_class = UpdateMentorDetailsSerializer
    queryset = Mentor.objects.all()
    permission_classes = (IsMentor,)

    def get(self, request, mentor_id):
        """
        This function is used to getting the mentor with particular mentor id
        :param request: mentor_id
        :return: returned the mentor data
        """
        mentor = Mentor.objects.filter(pk=mentor_id)
        if mentor:
            serializer = DisplayMentorCourseSerializer(mentor, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error("Mentor not found")
        return Response("Mentor Not Found", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, mentor_id):
        """
        This function is used to update the mentor data
        :param request: mentor id
        :return: update the mentor data
        """
        try:
            mentor = Mentor.objects.get(pk=mentor_id)
        except:
            logger.error("Mentor not found")
            return Response("Mentor not Found")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        courses = serializer.validated_data['course']
        for course_name in courses:
            course = Course.objects.get(course_name=course_name)
            mentor.course.add(course.id)
            mentor.save()
        logger.info("Course added successfully")
        return Response("Course Added SuccessFully")


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
        mentor = Mentor.objects.all()
        serializer = self.serializer_class(mentor, many=True)
        logger.info("Display Mentors list")
        return Response(serializer.data, status=status.HTTP_200_OK)

# class StudentMentorAPI(GenericAPIView):
#     serializer_class = StudentMentorSerializer
#
#     def put(self,request,student_id):
#         student = Student.objects.get(id=student_id)
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         mentors = serializer.validate_data['mentor']
#         for mentors in mentors:
#             stud_mentor = Mentor.objects.get(mentor=mentors)
#             student.mentor.add(stud_mentor.id)
#             student.save()
#         return Response("Mentor added successfully")
