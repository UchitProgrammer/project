from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('',views.home,name='home'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('faculty_index/',views.faculty_index,name='faculty_index'),
    path('faculty_changepassword/',views.faculty_changepassword,name='faculty_changepassword'),
    path('mystudents/',views.mystudents,name='mystudents'),
    path('changestatus/<int:pk>',views.changestatus,name='changestatus'),
    path('addcourse/',views.addcourse,name='addcourse'),
    path('addquestion/',views.addquestion,name='addquestion'),
    path('exam/',views.exam,name='exam',), 
    path('exam_instructions/<str:cname>/',views.exam_instructions,name='exam_instructions'),
    path('startexam/<str:cname>/',views.startexam,name='startexam'),
    path('examcheck',views.examcheck,name='examcheck'),
    path('myresult/',views.myresult,name='myresult'),
    path('studentsresult/',views.studentsresult,name='studentsresult'),
    path('faculty_profile/',views.faculty_profile,name='faculty_profile'),


]