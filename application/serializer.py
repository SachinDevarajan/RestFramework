from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def valid_age(self, age):
        if age <18:
            raise serializers.ValidationError('Age Must be more than 18')
        return age

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'fees']

    def validate_fees(self,fees):
        if fees <= 0:
            raise serializers.ValidationError("Fees must be greater than 0")
        return fees


class CourseDetailSerializer(CourseSerializer):
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['description','duration']

    