from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    place = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'student'


class Course(models.Model):
    name = models.CharField(max_length=100)
    duration = models.TextField()
    fees = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'course'


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)