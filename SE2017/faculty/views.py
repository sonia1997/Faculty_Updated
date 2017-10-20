from __future__ import unicode_literals
from django.template.context import RequestContext
from home.models import Workbooks
import json as simplejson
from django.http import HttpResponse
import json
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import loader
from django.shortcuts import render_to_response
from home.models import *
from home.models import Assignment
from .forms import UploadFileForm


def ViewProfs(request):
    CourseList = []
    if request.user.personnel.Role.Role_name == 'Faculty':
	request.session['Prof_Name']=request.user.username
        person_id = request.user.personnel.Person_ID
        IC = Instructors_Courses.objects.all()
        for i in range(0, len(IC)):
            if person_id == IC[i].Inst_ID.Person_ID:
                CourseList.append(IC[i].Course_ID.Course_Name)
	if CourseList==[]:
            flag=0
	    
	else:
            flag=1
    template = loader.get_template('prof.html')
    context = {'flag':flag,'Courses':CourseList,'Prof_Name':request.session['Prof_Name']}
    return HttpResponse(template.render(context, request))
def CoursePage(request):		
	if request.POST.get('action')=='Save':
		course=Courses.objects.get(Course_Name=request.session['course'])
		course.Course_description = request.POST.get('coursedes')
        	course.save()		
	elif request.POST.get('action')=="submit":
		request.session['course'] =request.POST.get('dropdown')
	course=Courses.objects.get(Course_Name=request.session['course']) 				
    	template = loader.get_template('prof1.html')
    	context = {'Course':course,'CourseName':request.session['course']}
    	return HttpResponse(template.render(context, request))
	
				
		
		
	

def ViewRegisteredStudents(request):
    studentlist = []
    course_name = request.GET.get('name')
    students = Students_Courses.objects.all()
    for student in students:
        if course_name == student.Course_ID.Course_Name:
            studentlist.append(student.Student_ID.LDAP.username)
    template = loader.get_template('student.html')
    context = {'Students': json.dumps(studentlist), 'Course': course_name}
    return HttpResponse(template.render(context, request))


def AddAssignment(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            courses = Courses.objects.all()
            for corse in courses:
                if corse.Course_Name == request.session['course']:
                    course = Courses.objects.get(Course_Name=corse.Course_Name)
                    break
            instance = Assignment(Course_ID=course, Assignment_File=request.FILES['file'])
            instance.save()
	     
	    
    else:
        CourseList = []
        form = UploadFileForm()
        
    return render(request, 'forms.html',
                 {'CourseName':request.session['course'], 'form': form, 'request': request})


def delete(request):
    if request.method != 'POST':
        raise Http404
    docId = request.POST.getlist('Assignment_File[]')
    for did in docId:
        docToDel = get_object_or_404(Assignment, Assign_ID=did)
        docToDel.Assignment_File.delete()
        docToDel.delete()
    return HttpResponse("Your File has been deleted successfully!!! ")


def Delass(request):
     asslist = []
     Assignments = Assignment.objects.all()
     for ass in Assignments:
     	if ass.Course_ID.Course_Name ==request.session['course']:
        	asslist.append(ass)
     return render(request, 'assignment.html', {'Assignments': asslist,'CourseName':request.session['course']})
   


def EditCourseDescription(request):
    if request.method == 'POST':
        course = request.POST.get('dropdown')
        courseobj = Courses.objects.get(Course_Name=course)
        courseobj.Course_description = request.POST.get('coursedes')
        courseobj.save()

        return HttpResponse("Successfully updated!!!")
    


def OfferCourses(request):
    if request.method == 'POST':
        person_id = request.user.personnel.Person_ID
        person = Personnel.objects.get(Person_ID=person_id)
        courseids = request.POST.getlist('courses[]')
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        for cid in courseids:
            corse = Courses.objects.get(Course_ID=cid)
            IC = Instructors_Courses(Course_ID=corse, Inst_ID=person, Start_Date=startdate, End_Date=enddate)
            IC.save()
    else:
        IC = Instructors_Courses.objects.all()
        IClist = []
        for ic in IC:
            IClist.append(ic.Course_ID)
        person_id = request.user.personnel.Person_ID
        courses = Courses.objects.all()
        courses1 = []
        for corse in courses:
            if corse not in IClist:
                courses1.append(corse)
        template = loader.get_template('reg.html')
        context = {'Courses': courses1,'CourseName':request.session['course'], 'IC': IClist, 'Prof_Name': request.user.username}
    return HttpResponse(template.render(context, request))
def ViewAttendance(request):	
    	studentcount={}
	sessioncount=0
	students=Attendance.objects.all()
    	classes=Attendance_Session.objects.all()
	for Class in classes:
		if Class.Course_Slot.Course_ID.Course_Name==request.session['course']:
			sessioncount=sessioncount+1
		
	for student in students:
		value=[0,1]
		value[0]=student.Student_ID.LDAP.username
		value[1]=0
		studentcount[student.Student_ID.Person_ID]=value	
	for student in students:
		if student.ASession_ID.Course_Slot.Course_ID.Course_Name==request.session['course'] and student.Marked=='A':
			studentcount[student.Student_ID.Person_ID][1]=studentcount[student.Student_ID.Person_ID][1]+1
	if request.method=="POST":
		return HttpResponse(request.POST.get('abc'))			    
    	template = loader.get_template('attendance.html')
    	context = {'classes':studentcount,'CourseName':request.session['course'],'workingdays':sessioncount}
    	return HttpResponse(template.render(context, request))	
def EnterMarks(request):
	assignidlist=[]
	idlist=[]
	studentlist=[]
	studentdict={}
	assignid=Assignment.objects.all()
	students=Students_Courses.objects.all()
	
	for assign in assignid:
		if assign.Course_ID.Course_Name==request.session['course']:
			assignidlist.append(assign.Assign_ID)
	for student in students:
		if student.Course_ID.Course_Name==request.session['course']:
			studentlist.append(student)
			studentdict[student.Student_ID.Person_ID]=[]
	for i in range(1,len(assignid)+1):
		idlist.append(i)
	if request.method=="POST":
		return HttpResponse(request.POST.get('assign'))
	template = loader.get_template('marks.html')
    	context = {'assignid':idlist,'CourseName':request.session['course'],'students':studentlist,'studentdict':studentdict}
    	return HttpResponse(template.render(context, request))
def index(request):
    template = 'sheet.html'
 
    app_action = request.POST.get('app_action')
    posted_data = request.POST.get('json_data')
 
    if posted_data is not None and app_action == 'save':
        this_sheet = request.POST.get("sheet")
        this_workbook = request.POST.get("workbook_name")
        sheet_id = request.POST.get("sheet_id")
 
        posted_data = json.dumps(posted_data)
 
        if(sheet_id):
            wb = Workbooks(id=sheet_id, workbook_name=this_workbook, 
                   sheet_name=this_sheet, data=posted_data)
        else:
            wb = Workbooks(workbook_name=this_workbook, 
                   sheet_name=this_sheet, data=posted_data)
        wb.save()
 
    elif app_action == 'get_sheets':
        wb_name = request.POST.get('workbook_name')
        sheets = Workbooks.objects.filter(workbook_name=wb_name)
 
        # use list comprehension to create python list which is like a JSON object
        sheets = [{ "sheet_id":i.id, "workbook_name": i.workbook_name.encode("utf-8"),
                    "sheet_name": i.sheet_name.encode("utf-8"), 
                    "data": json.loads(i.data.encode("utf-8"))} for i in sheets ]
 
        # dumps -> serialize to JSON
        sheets = json.dumps(sheets)
 
        return HttpResponse( sheets, mimetype='application/javascript' )
 
    elif app_action == 'list':
        workbooks = Workbooks.objects.values('workbook_name').distinct()
 
        # use list comprehension to make a list of just the work books names
        workbooks = [ i['workbook_name'] for i in workbooks ]
 
        # encode into json format before sending to page
        workbooks = json.dumps(workbooks)
 
        # We need to return an HttpResponse object in order to complete
        # the ajax call
        return HttpResponse( workbooks, mimetype='application/javascript' )
 
    return render(request, template,{})
