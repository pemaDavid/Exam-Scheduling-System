
from django.urls import path 
from . import views

urlpatterns = [
    
      path('', views.home, name='home'),
      path('login/', views.login_view, name='login'),
      path('faculty/', views.displayexamtabletofaculty, name='faculty'),
      path('dashboard/', views.dashboard, name='dashboard'),
      path('classroom/', views.classroom, name='classroomtable'),
      path('module/', views.module, name='moduletable'),
      path('invigilator/', views.invigilator, name='invigilatortable'),
      path('addInvigilator/', views.addInvigilator, name='addinvigilator'),
      path('student/', views.student,name='studentable'),
      path('generate/', views.generateTimetable, name = 'generate'),
      path('edit/',views.editable, name='editable'),
      path('publish/',views.displayexamtabletodashboard, name='dashtable'),
      path('viewtable/',views.viewtable, name='viewtable'),
      path('viewclassroom/',views.viewclassroomallocation, name='classroom'),
      path('viewinvigilation/',views.viewinvigilation, name='invigilation'),
      path('examinationschedule/',views.displayexamtabletopublic, name='schedule'),
      path('programme/',views.program, name='program'),
      path('department/',views.department, name='department'),
      path('modulemapping/',views.modulemap, name='modulemap'),
      path('studentrepeats/',views.repeats, name='repeats'),
      path('profile/',views.profile, name='profile'),
      path('generateClassroomAllocation/',views.generateclassroomallocation, name='generateclassroomallocation'),
      path('search/', views.search_results_view, name='search'),

      path('delete_student', views.delete_student, name="delete-student"),



    
]