from django.conf.urls import url

from . import views

app_name='faculty'
urlpatterns =[
	
         url(r'^ViewProfs/$',views.ViewProfs,name='ViewProfs'),
 url(r'^ViewAttendance/$',views.ViewAttendance,name='ViewAttendance'),   
url(r'^ViewRegisteredStudents/$',views.ViewRegisteredStudents,name='ViewRegisteredStudents'), 
url(r'^AddAssignment/$',views.AddAssignment,name='AddAssignment'),   
url(r'^Delass/$',views.Delass,name='Delass'),  
url(r'^delete/$',views.delete,name='delete'), 
url(r'^offercourses/$',views.OfferCourses,name='OfferCourses'), 
url(r'^editdescription/$',views.EditCourseDescription,name='EditCourseDescription'), 
url(r'^coursepage/$',views.CoursePage,name='CoursePage'),
url(r'^entermarks/$',views.EnterMarks,name='index'), 
        
        
	
    ]

