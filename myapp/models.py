from django.db import models
from django.utils import timezone

# Create your models here.

class Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	message=models.TextField()

	def __str__(self):
		return self.name


class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	mobile=models.CharField(max_length=100)
	address=models.TextField()
	password=models.CharField(max_length=100)
	profilepicture=models.ImageField(upload_to="profilepicture/",default="")
	usertype=models.CharField(max_length=100,default="student")
	status=models.CharField(max_length=100,default="pending")

	def __str__(self):
		return self.fname+" - "+self.lname

class Faculty_Subject(models.Model):
	CHOICE=(
			('python','python'),
			('Java','Java'),
			('C++','C++'),
			('PHP','PHP'),
		)
	faculty=models.ForeignKey(User,on_delete=models.CASCADE)
	subject=models.CharField(max_length=100,choices=CHOICE)

	def __str__(self):
		return self.faculty.fname

class Course(models.Model):
	faculty=models.ForeignKey(User,on_delete=models.CASCADE)
	cname=models.CharField(max_length=100)

	def __str__(self):
		return self.faculty.fname+" - "+self.cname
	
class Questions(models.Model):
	cname=models.ForeignKey(Course,on_delete=models.CASCADE)
	question=models.CharField(max_length=200,default="")
	op1=models.CharField(max_length=100)
	op2=models.CharField(max_length=100)
	op3=models.CharField(max_length=100)
	op4=models.CharField(max_length=100)
	answer=models.CharField(max_length=100,default="")

	def __str__(self):
		return self.question

class Results(models.Model):
	student=models.ForeignKey(User,on_delete=models.CASCADE)
	course=models.ForeignKey(Course,on_delete=models.CASCADE)
	marks=models.PositiveIntegerField()
	date=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.student.fname





