from rest_framework import status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from Authentication.permissions import IsStudent, IsMentor
from learning_management.models import *
from learning_management.serializer import AddCourseSerializer, UpdateStudentDetailsSerializer, \
    UpdateMentorDetailsSerializer, UpdateStudentEducationSerializer, StudentMentorSerializer


class AddCourseAPI(GenericAPIView):
    serializer_class = AddCourseSerializer
    queryset = Course.objects.all()

    def get(self, request):
        course = Course.objects.all()
        serializer = self.serializer_class(course, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        serializer.save()
        return Response("New Course is Added ", status=status.HTTP_201_CREATED)


class UpdateStudentDetailsAPI(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateStudentDetailsSerializer
    permission_classes = (IsStudent,)
    queryset = Student.objects.all()
    lookup_field = 'id'

    def get_object(self):
        return self.request.user.student

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UpdateStudentEducationAPI(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateStudentEducationSerializer
    permission_classes = (IsStudent,)
    queryset = Student.objects.all()
    lookup_field = 'id'

    def get_object(self):
        return Education.objects.get(student=self.request.user.student)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class UpdateMentorDetailsAPI(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateMentorDetailsSerializer
    permission_classes = (IsMentor,)
    queryset = Mentor.objects.all()
    lookup_field = 'id'

    def get_object(self):
        return self.request.user.mentor

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

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