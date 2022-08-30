from django.db import models

# Create your models here.

class Lecturer(models.Model):
    TITLES = [
        ('PROF.DR', 'prof.dr'),
        ('DOC', 'Doc'),
        ('DR', 'Dr'),
    ]
    
    user_id = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=10, choices=TITLES)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    mail = models.EmailField()

    last_update = models.DateTimeField(auto_now=True)

class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)
    course_name = models.CharField(max_length=255)
    instructor = models.ForeignKey(Lecturer, on_delete=models.PROTECT)
    #teaching_asistan = models.ForeignKey(Lecturer, on_delete=models.PROTECT)
    student_number = models.PositiveIntegerField()
    
class Exam(models.Model):
    exam_id = models.CharField(max_length=10, primary_key=True)
    exam_date = models.DateField()
    exam_timeslot = models.IntegerField()
    course_id = models.OneToOneField(Course, on_delete=models.PROTECT)
    room = models.CharField(max_length=10)
    req_inv = models.PositiveSmallIntegerField()
    exam_weight = models.FloatField()
    