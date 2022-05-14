from django.shortcuts import render,redirect
from . models import User,Course,Questions,Results,Faculty_Subject,Contact
from django.http import JsonResponse
import random
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
	return render(request,'index.html')

def index(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=="student":
			return render(request,'index.html')
		else:
			return render(request,'faculty_index.html')
	except:
		return render(request,'index.html')

def aboutus(request):
	return render(request,'about.html')
	
def faculty_index(request):
	return render(request,'faculty_index.html')

def contact(request):
	if request.method=="POST":
		Contact.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			mobile=request.POST['mobile'],
			message=request.POST['message'],
			)
		msg="""Contact saved successfully.
				Our Staff contact you soon.
				 Thank You for contacting us."""
		return render(request,'contact.html',{'msg':msg})
	else:
		return render(request,'contact.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email is already registered."
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
							usertype=request.POST['usertype'],
							fname=request.POST['fname'],
							lname=request.POST['lname'],
							email=request.POST['email'],
							mobile=request.POST['mobile'],
							address=request.POST['address'],
							password=request.POST['password'],
							profilepicture=request.FILES['profilepicture']
					)
				msg="User Sign Up Sucessfully."
				return render(request,'login.html',{'msg':msg})
			else:
				msg="Password and Confirm Password does not match."
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(
								email=request.POST['email'],
								password=request.POST['password']
								)
			if user.status=="pending":
				msg="Student Status is pending."
				return render(request,'login.html',{'msg':msg})
			elif user.usertype=="student":
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profilepicture']=user.profilepicture.url
				return render(request,'index.html')
			else:
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profilepicture']=user.profilepicture.url
				return render(request,'faculty_index.html')
		except:
			msg="Email_Id or Password is incorrect."
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['password']
		return render(request,'login.html')
	except:
		return render(request,'login.html')		

def changepassword(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['opassword']:
			if request.POST['npassword']==request.POST['cpassword']:
				user.password=request.POST['npassword']
				user.save()
				return redirect('logout')
			else:
				msg="New Password and Confirm Password does not match."
				return render(request,'changepassword.html',{'msg':msg})
		else:
			msg="Old Password is not correct."
			return render(request,'changepassword.html',{'msg':msg})
	else:
		return render(request,'changepassword.html')

def faculty_changepassword(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['opassword']:
			if request.POST['npassword']==request.POST['cpassword']:
				user.password=request.POST['npassword']
				user.save()
				return redirect('logout')
			else:
				msg="New Password and Confirm Password does not match."
				return render(request,'faculty_changepassword.html',{'msg':msg})
		else:
			msg="Old Password is not correct."
			return render(request,'faculty_changepassword.html',{'msg':msg})
	else:
		return render(request,'faculty_changepassword.html')

def mystudents(request):
	students=User.objects.filter(usertype="student")
	return render(request,'mystudents.html',{'students':students})

def changestatus(request,pk):
	student=User.objects.get(pk=pk)
	student.status="approved"
	student.save()
	return redirect('mystudents')

def addcourse(request):
	if request.method=="POST":		
		courses=Course.objects.all()
		if courses.filter(cname=request.POST['cname']):
			msg="Course is already added."
			return render(request,'addcourse.html',{'msg':msg,'courses':courses})
		else:
			faculty=User.objects.get(email=request.session['email'])
			Course.objects.create(
						faculty=faculty,
						cname=request.POST['cname'],
				)
			msg="Course add successfully"		
			courses=Course.objects.all()
			return render(request,'addcourse.html',{'msg':msg,'courses':courses})
	else:		
		courses=Course.objects.all()
		return render(request,'addcourse.html',{'courses':courses})

def addquestion(request):
	courses=Course.objects.all()
	if request.method=="POST":		
		cname=Course.objects.get(pk=request.POST['cname'])
		Questions.objects.create(
					cname=cname,
					question=request.POST['question'],
					op1=request.POST['op1'],
					op2=request.POST['op2'],
					op3=request.POST['op3'],
					op4=request.POST['op4'],
					answer=request.POST['answer']
			)
		msg="Question add successfully"
		return render(request,'addquestion.html',{'courses':courses,'msg':msg})
	else:
		return render(request,'addquestion.html',{'courses':courses})

def exam(request):
	courses=Course.objects.all()
	return render(request,'exam.html',{'courses':courses})

def exam_instructions(request,cname):
	return render(request,'exam_instructions.html',{'cname':cname})

def startexam(request,cname):
	courses=Course.objects.get(cname=cname)
	questions=Questions.objects.filter(cname=courses)
	questions=set(questions)
	que=random.sample(questions,4)
	return render(request,'startexam.html',{'questions':que})
	
def examcheck(request):
	user=User.objects.get(email=request.session['email'])
	l=list(request.POST.items())[1:]
	marks=0
	for i in l:
		question=Questions.objects.get(pk=i[0])
		course=Course.objects.get(cname=question.cname.cname)
		if question.answer==i[1]:
			marks=marks+1
	result=Results.objects.create(
				student=user,
				course=course,
				marks=marks,
		)

	subject = 'Exam Results'
	message = 'You have given course '+result.course.cname+' exam.\n You have obtain '+str(result.marks)+' Marks out of 4.'
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [user.email, ]
	send_mail( subject, message, email_from, recipient_list )
	return redirect('myresult')

def myresult(request):
	student=User.objects.get(email=request.session['email'])
	result=Results.objects.filter(student=student)
	return render(request,'myresult.html',{'result':result})

def studentsresult(request):
	faculty=User.objects.get(email=request.session['email'])
	faculty_subject=Faculty_Subject.objects.filter(faculty=faculty)
	course=Course.objects.get(faculty=faculty)
	result=Results.objects.filter(course=course)
	return render(request,'studentsresult.html',{'result':result})

def faculty_profile(request):
	faculty=User.objects.get(email=request.session['email'])
	faculty_subject=Faculty_Subject.objects.filter(faculty=faculty)

	if request.method=="POST":
		try:
			Faculty_Subject.objects.get(faculty=faculty,subject=request.POST['subject'])
			msg="Subject is allready selected."
			return render(request,'faculty_profile.html',{'faculty_subject':faculty_subject,'msg':msg})
		except:
			Faculty_Subject.objects.create(
						faculty=faculty,
						subject=request.POST['subject']
			)
		msg="Subject Add Successfully"
		return render(request,'faculty_profile.html',{'faculty_subject':faculty_subject,'msg':msg})
	else:
		return render(request,'faculty_profile.html',{'faculty_subject':faculty_subject})











