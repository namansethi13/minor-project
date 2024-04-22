from django.shortcuts import render
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import *
import uuid
from django.contrib.auth.decorators import login_required
import os
from django.core.files.base import File
from django.views.decorators.csrf import csrf_exempt
from .format1 import *
from django.utils.encoding import smart_str
from .format2 import *
from .format6 import *
from .format7 import *
def normalize_page(request):
    return render(request, 'normalize.html')

from .conversions import ResultProcessor
@csrf_exempt
def normalize(request):
    #elective
    #df
    
    os.makedirs(os.path.join(os.path.dirname(__file__), "buffer_files"), exist_ok=True)
    
    
    try:
        subjects=Subject.objects.filter(course=request.POST['course'],semester=request.POST['semester'])
        subject_name_mapping={}
        credits_mapping={}
        exclude_subject_dict={}
       
        
        headers_to_add=json.loads(request.POST['headers_to_add'])
        footers_to_add=json.loads(request.POST['footers_to_add'])
        for subject in subjects:
            subject_name_mapping[f"{subject.code}({subject.credit})"]=f"{subject.code} {subject.subject} (Internal)"
            subject_name_mapping[f"{subject.code}({subject.credit}).1"]=f"{subject.code} {subject.subject} (External)"
            subject_name_mapping[f"{subject.code}({subject.credit}).2"]=f"{subject.code} {subject.subject} (Total)"
            
        
        for subject in subjects:
           
            credits_mapping[f"{subject.code} {subject.subject} (Total)"]=subject.credit
        for subject in subjects:
            if subject.is_not_university:
                exclude_subject_dict[f"{subject.code}"]=subject.subject
      
        
        
        random_file_name = uuid.uuid4().hex[:6].upper()
        try:
            
            processor = ResultProcessor(request.FILES.get("excel_file"),f'{random_file_name}.xlsx', subject_name_mapping, exclude_subject_dict,footers_to_add , headers_to_add,credits_mapping)
           
            processor.read_data()
            
            processor.rename_columns()
            
            processor.calculate_total()
            
            processor.calculate_cgpa()
            
            processor.process_reappear()
            
            processor.process_absents()
            
            processor.update_reappear_absent_columns()
            
            processor.final_rename_columns()
            
            is_saved,result_df = processor.save_result()
           
        except Exception as e:
            print(e)
            return HttpResponse("Something went wrong", status=500)
        if is_saved:
            
            
            with open(os.path.join(os.path.dirname(__file__), "buffer_files", f"{random_file_name}.xlsx"), "rb") as excel:

                file_object = File(excel)
                result_json = result_df.to_json()
                course = Course.objects.get(id=request.POST['course'])
                instance=Result.objects.create(course=course,passout_year=request.POST['passing'],semester=request.POST['semester'],xlsx_file=file_object,result_json=result_json)
            
            
            
            file_path = os.path.join(os.path.dirname(__file__), "buffer_files", f"{random_file_name}.xlsx")
            os.remove(file_path)
            response = HttpResponse("saved successfully")
        
            return response
            
            
        else:
            response = HttpResponse("Something went wrong", status=500)
        
            return response
        
    except Exception as e:
        print(e)
        response = HttpResponse(f"Something went wrong : {e}", status=500)
        
        return response
    

@csrf_exempt
def check_result(request):
    
    
    course , passing = json.loads(request.body)['course'] , json.loads(request.body)['passing']
    try:
        semesters = Result.objects.filter(course=course,passout_year=passing)
    
    except Result.DoesNotExist:
        
        return HttpResponse("no result found",status=404)
   
    semester_id={}
    for s in semesters:
        semester_id[s.semester]=s.id
        
    return HttpResponse(
        json.dumps(semester_id),
        content_type="application/json"
    )

@login_required
def convert(request):
    return render(request, 'convert.html' , {'total_semesters':[1,2,3,4,5,6]})

def download_result(request,id):
    try:
        result = Result.objects.get(id=id)
    except Result.DoesNotExist:
        return HttpResponse("no result found",status=404)
    
    response = HttpResponse(result.xlsx_file, content_type='application/ms-excel')
    response['Content-Disposition'] = f"attachment; filename={result}.xlsx"
    return response
@csrf_exempt
def update_result(request):
    
    course , passing ,semester = request.POST["course"] , request.POST["passing"] ,request.POST["semester"]
    updated_result=request.FILES.get("updated_excel_file")
    try:
        result = Result.objects.get(course=course,passout_year=passing,semester=semester)
        result.xlsx_file=updated_result
        result.save()
    except Exception as e:
        return HttpResponse("Something went wrong", status=500)
    return HttpResponse("updated successfully")
@csrf_exempt
def format1(request):
    if request.method=="GET":
        semester = request.GET.get("semester")
        course = request.GET.get("course")
        all_subjects = Subject.objects.filter(course=course.upper(),semester=semester)
        
        subject_code_name_mapping = {subject.code:subject.subject for subject in all_subjects}
        return HttpResponse(json.dumps(subject_code_name_mapping),content_type="application/json")
        
        
        
    if request.method=="POST": 
        data = request.body
        data = json.loads(data)
        
        file_data = {}
        faculty_name = ""
        shift = ""
        all_subjects = {}
        semester = ""
        year = ""
        for e in data:
            entry = data[e]
            xlsxfile = Result.objects.get(course=entry['course'],passout_year=entry['passing'],shift=entry['shift'],semester=entry['semester']).xlsx_file
            try:
                all_subjects_objects = Subject.objects.filter(course=entry['course'],semester=entry['semester'])
            except Subject.DoesNotExist:
                return HttpResponse("no result found",status=404)
            semester = entry['semester']
            year = entry['passing']
            all_subjects.update({subject.code:subject.subject for subject in all_subjects_objects})
            file_data[xlsxfile] = {
                "all_columns": [subject.code for subject in all_subjects_objects],
                "section-subject": entry['section-subject'],
                "course": entry['course'],
            }
            faculty_name = entry['faculty_name']
            shift = entry['shift']
        format1 = f1(file_data=file_data,all_subjects=all_subjects,faculty_name=faculty_name,shift=shift,semester=semester,passing=year)
        file_name = format1.write_to_doc()
        file_path = os.path.join(os.path.dirname(__file__), "buffer_files", file_name)
        with open(file_path, "rb") as word:
            data = word.read() 
            response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={smart_str(file_name)}'
        os.remove(os.path.join(os.path.dirname(__file__), "buffer_files", file_name))
        return response

@csrf_exempt
def format2(request):
    if request.method == "POST":
        data = request.body
        data = json.loads(data)
        subject_teacher_mapping = data['subjectTeacherMapping']
        
        faculty_name = data['faculty_name']
        semester = data['semester']
        course = data['course']
        shift = data['shift']
        section = data['section']
        batch = data['batch']
        passout_year = data['passing']
        if(int(semester)%2==0):
            month="Jan-July"
        else:
            month="Aug-Dec"
        try:
            all_subjects = Subject.objects.filter(course=course,semester=semester)
            all_subjects = {subject.code:subject.subject for subject in all_subjects}
            xlsxfile = Result.objects.get(course=course,passout_year=passout_year,shift=shift,semester=semester).xlsx_file
        except Exception as e:
            return HttpResponse("Something went wrong", status=500)
        subject_codes = list(all_subjects.keys())
        format2 = Format_2(xlsxfile,all_subjects,course,semester,shift,section,batch,passout_year,faculty_name,month)
        format2.read_data(subject_codes,section)
        format2.read_from_filtered_excel(course,subject_teacher_mapping)
        file_name = format2.write_to_doc()
        with open(os.path.join(os.path.dirname(__file__), "buffer_files", file_name), "rb") as word:
            data = word.read() 
            response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={smart_str(file_name)}'
        os.remove(os.path.join(os.path.dirname(__file__), "buffer_files", file_name))
        return response
        
    if request.method == "GET":
        semester = request.GET.get("semester")
        course = request.GET.get("course")
        
        all_subjects = Subject.objects.filter(course=course.upper(),semester=semester)
        
        subject_teacher_mapping = {subject.code:"DR. ABC" for subject in all_subjects}
        subject_code_mapping = {subject.code:subject.subject for subject in all_subjects}
        return HttpResponse(json.dumps([subject_teacher_mapping,subject_code_mapping]),content_type="application/json")

@csrf_exempt
def format6(request):
    
    data=request.body
    data=json.loads(data)
    file_data={}
    valuedict={}
    flag=1
    all_courses=[]
    admitted_years=[]
    all_semesters=[]
    keysofdata=data.keys()
    dict_of_all_subjects={}
    for i,key in enumerate(keysofdata):
        semester,course=key.split('_')
        faculty_name=data[key]['faculty_name']
        if(int(semester)%2==0):
            month="Jan-July"
        else:
            month="Aug-Dec"
        all_semesters.append(semester)
        
        admitted_years.append(data[key]['admitted'])
        
        try:
            Resultobject=Result.objects.get(course=course,passout_year=data[key]['passing'],shift=data[key]['shift'],semester=semester)
        except Exception as e:
            return HttpResponse("Something went wrong", status=500)
        
        try:
            all_subjects=Subject.objects.filter(course=course,semester=semester)
        except Exception as e:
            return HttpResponse("Something went wrong", status=500)
    
        valuedict['subjects']=[subject.code for subject in all_subjects]
        
        valuedict['needed_subjects']=data[key]['needed_subjects']
        
        valuedict['sections']=data[key]['sections']
        valuedict['course']=course
        all_courses.append(course)
        
        if data[key]['shift']==1:
            valuedict['shift']='M'
        else:
            valuedict['shift']='E'
        
        valuedict['semester']=semester
        file_data[Resultobject.xlsx_file]=valuedict
        valuedict={}
        
        dict_of_all_subjects.update({
            subject.code:subject.subject for subject in all_subjects
        })
    
     
    common_letters = []
    for i in range(len(all_courses)):
      if i == 0:
        common_letters = list(all_courses[i])
    else:
        common_letters = [letter for letter in common_letters if letter in all_courses[i]]


    common_letters_string = ''.join(common_letters)
    f6 = Format6(file_data,dict_of_all_subjects,faculty_name=faculty_name,shift='M' if data[key]['shift']==1 else 'E',passing=data[key]['passing'],course=common_letters_string,month=month,admitted_years=admitted_years,all_semesters=all_semesters)
    file_name =f6.write_to_doc()
    with open(os.path.join(os.path.dirname(__file__), "buffer_files", file_name), "rb") as word:
                data = word.read() 
                response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = f'attachment; filename={smart_str(file_name)}'
    os.remove(os.path.join(os.path.dirname(__file__), "buffer_files", file_name))
    return response
    
    



@csrf_exempt
def format7(request):
    if request.method == "GET":
        semester = request.GET.get("semester")
        course = request.GET.get("course")
        all_subjects = Subject.objects.filter(course=course.upper(),semester=semester)
        subject_list = {subject.code:subject.subject for subject in all_subjects}
        practical_subject_list = {subject.code:subject.subject for subject in all_subjects if subject.is_practical}
        
        response = {
    
        "Subjects": subject_list,
        "Faculty Names": ["DR. ABC" for subject in all_subjects],
        "Practicals": practical_subject_list,
        "Section":"",
        "Semester": semester,
    
}
        return HttpResponse(json.dumps(response),content_type="application/json")
    if request.method == "POST":
        data = request.body
        data = json.loads(data)
        subject_teacher_mapping = data
        course = data['course']
        semester = data['semester']
        shift = data['shift']
        passout_year = data['passing']
        faculty_name = data['faculty_name']
        admitted = data['admitted']
        xlsxfile = Result.objects.get(course=course,passout_year=passout_year,shift=shift,semester=semester).xlsx_file
        try:
            all_subjects = Subject.objects.filter(course=course,semester=semester)
        except Exception as e:
            return HttpResponse("Something went wrong", status=500)
        all_subjects_dict = {subject.code:subject.subject for subject in all_subjects}
        format7 = Format7(xlsxfile,data,faculty_name,all_subjects_dict,admitted)
        file_name = format7.write_to_doc()
        with open(os.path.join(os.path.dirname(__file__), "buffer_files", file_name), "rb") as word:
            data = word.read() 
            response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={smart_str(file_name)}'
        os.remove(os.path.join(os.path.dirname(__file__), "buffer_files", file_name))
        return response
    
    
    
   
    
    
    
    
    
    
    
    

    