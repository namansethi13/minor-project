from django.shortcuts import render
import json
# Create your views here.
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

def normalize_page(request):
    return render(request, 'normalize.html')

from .conversions import ResultProcessor
@csrf_exempt
def normalize(request):
    if not os.path.exists("results/buffer_files"):
        os.mkdir("results/buffer_files")
    print(request)
    print(request.FILES)
    
    try:
        subjects=Subject.objects.filter(course=request.POST['course'])
        subject_name_mapping={}
        credits_mapping={}
        exclude_subject_dict={}
       
        
        headers_to_add=json.loads(request.POST['headers_to_add'])
        footers_to_add=json.loads(request.POST['footers_to_add'])
        for subject in subjects:
            subject_name_mapping[f"{subject.code}({subject.credit})"]=f"{subject.code} {subject.subject} (Internal)"
            subject_name_mapping[f"{subject.code}({subject.credit}).1"]=f"{subject.code} {subject.subject} (External)"
            subject_name_mapping[f"{subject.code}({subject.credit}).2"]=f"{subject.code} {subject.subject} (Total)"
            
        print(subject_name_mapping)
        for subject in subjects:
           
            credits_mapping[f"{subject.code} {subject.subject} (Total)"]=subject.credit
        for subject in subjects:
            if subject.is_not_university:
                exclude_subject_dict[f"{subject.code}"]=subject.subject
      
        # headers_to_add = [["Maharaja Surajmal Institute"],
        #               ["BCA(M) Batch 2022-2025"],
        #               ["Class-: BCA  II Semester Batch [2022-2025]     Jan- June 2023"],
        #               ]
        # footers_to_add = [["102-Applied Maths Dr. Anchal Tehlan (Sec A & B)"],
        #               ["104-WBP - Mr. Sundeep Kumar(A) & Ms. Kanika Kundu (B)"],
        #               ["106-Data Struc Using C - Dr.Neetu Anand(A )   Mr.Manoj Kumar (B )"],
        #               ["108-DBMS - Ms.Kanika Kundu (A) & Ms.Vinita Tomar(B)"],
        #               ["110-EVS - Dr.Manju Dhillon (Sec A & Sec B)"],
        #               ["172-WBP Lab - Mr.Sundeep Kumar/ Dr.Neetu Narwal (Sec A) &  Ms.Kanika Kundu(Sec A) & Dr.Neetu Narwal (Sec B)"],
        #               ["174- DS Lab - Dr.Neetu Anand /Dr.Kumar Gaurav (A ) &  Mr.Manoj Kumar (B )"],
        #               ["176- DBMS Lab - Ms.Kanika Kundu / Mr. Siddharth Shankar (A)   &  Ms.Vinita Tomar (B)"],
        #               [""],
        #               ["Class Coordinator: Ms.Anchal Tehlan (Sec A) - Mr.Manoj Kumar (Sec B)"],
        #               ]
        
        random_file_name = uuid.uuid4().hex[:6].upper()
        processor = ResultProcessor(request.FILES.get("excel_file"),f'{random_file_name}.xlsx', subject_name_mapping, exclude_subject_dict,footers_to_add , headers_to_add,credits_mapping)
        processor.read_data()
        processor.rename_columns()
        processor.calculate_total()
        processor.calculate_cgpa()
        processor.process_reappear()
        processor.process_absents()
        processor.update_reappear_absent_columns()
        processor.final_rename_columns()
        is_saved = processor.save_result()
        if is_saved:
            
            print("saved")
            with open(f"results/buffer_files/{random_file_name}.xlsx", "rb") as excel:
                file_object = File(excel)
                instance=Result.objects.create(course=request.POST['course'],passout_year=request.POST['passing'],shift=request.POST['shift'],semester=request.POST['semester'],xlsx_file=file_object)
            
            print("created")
            os.remove(f"results/buffer_files/{random_file_name}.xlsx")
            response = HttpResponse("saved successfully")
        
            return response
            
            #data = None
            
            # with open(f"results/buffer_files/{random_file_name}.xlsx", "rb") as excel:
            #     data = excel.read()
            #     print("the value of one isssssssss", is_saved) 
            # os.remove(f"results/buffer_files/{random_file_name}.xlsx")
            # response = HttpResponse(data, content_type='application/ms-excel')
            # return response
        else:
            response = HttpResponse("Something went wrong")
        
            return response
        # return HttpResponse(one, content_type='application/pdf')    


        # one=one.convert()
        #converter.convert()
    except Exception as e:
        print(e)
    
    # print(one)

@csrf_exempt
def check_result(request):
    # request body contains JSON.stringify data
    print(json.loads(request.body))
    course , passing , shift = json.loads(request.body)['course'] , json.loads(request.body)['passing'] , json.loads(request.body)['shift']
    semesters = Result.objects.filter(course=course,passout_year=passing,shift=shift)
    print(list(semesters))
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
    result = Result.objects.get(id=id)
    print(result)
    response = HttpResponse(result.xlsx_file, content_type='application/ms-excel')
    response['Content-Disposition'] = f"attachment; filename={result}.xlsx"
    return response
@csrf_exempt
def update_result(request):
    print((request.POST["course"]))
    course , passing , shift,semester = request.POST["course"] , request.POST["passing"] , request.POST["shift"],request.POST["semester"]
    updated_result=request.FILES.get("updated_excel_file")
    result = Result.objects.get(course=course,passout_year=passing,shift=shift,semester=semester)
    result.xlsx_file=updated_result
    result.save()
    return HttpResponse("updated successfully")
@csrf_exempt
def format1(request):
    data=request.body
    data=json.loads(data)
    resultobjects=[]
    subjects=data['subjectcodes']
    list_of_subjectcodes=[]
    filedata={}
    course=data['course']
    shift=data['shift']
    faculy_name=data['faculty_name']
    for i,sem  in enumerate(data['semester']):
        resultobjects.append(Result.objects.get(course=course[i],passout_year=data['passing'][i],shift=shift,semester=data['semester'][i]))
        list_of_subjectcodes.append(list(Subject.objects.filter(course=course[i],semester=data['semester'][i]).values_list('code',flat=True)))
        print(list_of_subjectcodes[i])
        filedata[resultobjects[i].xlsx_file]=[data['sections'][i]]#append not working
        filedata[resultobjects[i].xlsx_file].extend(list(list_of_subjectcodes[i]))
        print(filedata)
    all_subjects={}
    for i,c in enumerate(course):
        
        all_subjects_objects=Subject.objects.filter(course=course[i])
        
        for obj in all_subjects_objects:
            all_subjects[obj.code]=obj.subject
    format1=f1(filedata,all_subjects=all_subjects,faculty_name=faculy_name,shift=shift)
    format1.process_data(subjects=subjects)
    format1.read_from_filtered_excel(course_name=course, subject_code=subjects)
    file_name = format1.write_to_doc()
    with open(f"results/buffer_files/{file_name}", "rb") as word:
        data = word.read() 
        response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={smart_str(file_name)}'
    os.remove(f"results/buffer_files/{file_name}")
    return response

@csrf_exempt
def format2(request):
    if request.method == "POST":
        data = request.body
        data = json.loads(data)
        subject_teacher_mapping = data['subjectTeacherMapping']
        print(subject_teacher_mapping)
        semester = data['semester']
        course = data['course']
        shift = data['shift']
        section = data['section']
        batch = data['batch']
        passout_year = data['passing']
        all_subjects = Subject.objects.filter(course=course,semester=semester)
        all_subjects = {subject.code:subject.subject for subject in all_subjects}
        xlsxfile = Result.objects.get(course=course,passout_year=passout_year,shift=shift,semester=semester).xlsx_file
        subject_codes = list(all_subjects.keys())
        format2 = Format_2(xlsxfile,all_subjects,course,semester,shift,section,batch,passout_year)
        format2.read_data(subject_codes,section)
        format2.read_from_filtered_excel(course,subject_teacher_mapping)
        file_name = format2.write_to_doc()
        with open(f"results/buffer_files/{file_name}", "rb") as word:
            data = word.read() 
            response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={smart_str(file_name)}'
        os.remove(f"results/buffer_files/{file_name}")
        return response
        
    if request.method == "GET":
        semester = request.GET.get("semester")
        course = request.GET.get("course")
        print(semester,course)
        all_subjects = Subject.objects.filter(course=course.upper(),semester=semester)
        print(all_subjects)
        subject_teacher_mapping = {subject.code:"DR. ABC" for subject in all_subjects}
        return HttpResponse(json.dumps(subject_teacher_mapping),content_type="application/json")

    
    
    
   
    
    
    
    
    
    
    
    

    