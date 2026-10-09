from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('',home,name='/'),
    path('students/',students,name='students'),
    path('view_students/',view_students,name='view_students'),
    path('auth/',obtain_auth_token,name='auth'),
    path('courses/',courses,name='courses'),
    path('add_course/',add_course,name='add_course'),
    
    path('token/',TokenObtainPairView.as_view(),name='token'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh'),
    path('login/',userlogin,name='login'),
    
    path('student_generic/',StudentGenericView.as_view(),name='student_generic'),
    path("student_generic_ud/<int:id>/",StudentGenericViewUD.as_view(),name='student_generic_ud'),
    path("student_retrieve/<int:id>/",StudentRetrieve.as_view(),name='student_retrieve')

]