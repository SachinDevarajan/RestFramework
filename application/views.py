from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from .tokens import *
from django.contrib.auth import authenticate

# Create your views here.

@api_view(['GET'])
def home(request):
    return Response({"status":200, "message":"This is Home Page"})


@api_view(['GET'])
def students(request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'message': 'Student Created Successfully',
                'data': serializer.data
            }, status=201)

        return Response(serializer.errors, status=400)
        


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def view_students(request):
    students = Student.objects.all().order_by('id')

    paginator = PageNumberPagination()
    paginator.page_size = 5 
    paginated_student = paginator.paginate_queryset(students,request)

    serialize = StudentSerializer(paginated_student, many = True)
    return paginator.get_paginated_response(serialize.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def courses(request):
    courses = Course.objects.all()
    serialize = CourseSerializer(courses,many=True)
    return Response(serialize.data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_course(request):
    serialize = CourseDetailSerializer(data = request.data)
    if serialize.is_valid():
        serialize.save()
        return Response({
             'message':'Course Created Successfully',
             'data':serialize.data
        },status=201)
    return Response(serialize.errors, status=400)


@api_view(['POST'])
def userlogin(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(
        username = username,
        password = password
    )
    if user:
        refresh = MyToken.for_user(user)
        return Response({
            'message':'Login Successful.....',
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        })
    return Response({'message':'user not found..!!!'})


class StudentGenericView(CreateAPIView, ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentGenericViewUD(UpdateAPIView, DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'

class StudentRetrieve(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'


