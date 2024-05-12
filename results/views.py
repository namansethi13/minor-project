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
from .format11 import *
from .format4 import *
from .format5 import *
from accounts.middleware import jwt_token_required
from .elective_df import *
def normalize_page(request):
    return render(request, 'normalize.html')

from .conversions import ResultProcessor

@csrf_exempt 
@jwt_token_required
def normalize(request):
    #elective
    #df
    
    os.makedirs(os.path.join(os.path.dirname(__file__), "buffer_files"), exist_ok=True)
    
    
    try:
        course = Course.objects.get(id=request.POST['course'])
        csv_file = request.FILES.get("excel_file")
        subjects=Subject.objects.filter(course=course,semester=request.POST['semester'])
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
        print("hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        '''''
        Creating datafrom with handeled elective in the below code
        '''''

        random_file_name = uuid.uuid4().hex[:6].upper()
        is_elective = request.POST.get("is_elective")
        json_data = None
        elective_df = None
        if is_elective.upper() == "true".upper():
            json_string_data = request.POST.get("json_string_data")
            json_data = json.loads(json_string_data)
           
            E = ElectiveDf(csv_file,subject_name_mapping=subject_name_mapping,exclude_subject_dict=exclude_subject_dict,credits_mapping=credits_mapping,is_elective=is_elective,elective_obj=json_data)
            elective_df = E.get_df()
        """
        creating excel file in below code
        """
        print("elective df creadted successfully")
        try:
            processor = ResultProcessor(csv_file ,f'{random_file_name}.xlsx', subject_name_mapping, exclude_subject_dict,footers_to_add , headers_to_add,credits_mapping)
            if is_elective.upper() == "true".upper():
                processor.initialize_for_elective_df(elective_df)
                is_saved,result_df = processor.save_result()
            else:
                processor.read_data()
                print("data read successfully")
                
                processor.rename_columns()
                print("columns renamed successfully")
                processor.calculate_total()
                print("total calculated successfully")
                processor.calculate_cgpa()
                print("cgpa calculated successfully")
                processor.process_reappear()
                print("reappear processed successfully")
                processor.process_absents()
                print("absents processed successfully")
                processor.update_reappear_absent_columns()
                print("reappear absent columns updated successfully")
                processor.final_rename_columns()
                print("final columns renamed successfully")
                is_saved,result_df = processor.save_result()
                print("result saved successfully")
        except Exception as e:
            print(e)
            return HttpResponse("Something went wrong", status=500)
        if is_saved:
            
            
            with open(os.path.join(os.path.dirname(__file__), "buffer_files", f"{random_file_name}.xlsx"), "rb") as excel:

                file_object = File(excel)
                if is_elective.upper() == "true".upper():
                    result_df = elective_df.copy()
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
# @jwt_token_required
def check_elective(request):
    csv_file = request.FILES.get("excel_file")
    df = pd.read_csv(csv_file)
    headings = list(df.columns)[4:]
    elective_headings = []
    for heading in headings:
        if "/" in heading:
            elective_headings.append(heading)
    if len(elective_headings) == 0:
        return HttpResponse(json.dumps({"status": False}), content_type="application/json")
    for elective in elective_headings:
       if ".1" in elective:
              elective_headings.remove(elective)
    for elective in elective_headings:
       if ".2" in elective:
              elective_headings.remove(elective)
    elective_between = []
    for elective in elective_headings:
       elective_tuple = tuple(elective.split("/"))
       elective_between.append(elective_tuple)
    enrollments = df.iloc[1:,1]
    enrollments = [f"{int(enrollment):011d}" for enrollment in enrollments]
    elective_list = []
    for elective_tuple in elective_between:
        temp = {}
        for elective in elective_tuple:
            temp[elective] = []
        elective_list.append(temp)
    course = request.POST.get("course")
    subjects=Subject.objects.filter(course=course,semester=request.POST['semester'])
    subject_name_mapping={}
    for subject in subjects:
        subject_name_mapping[f"{subject.code}({subject.credit})"]=f"{subject.subject}"
    enrollment_name_mapping = {}
    for i in range(1, len(enrollments)+1):
        enrollment_name_mapping[enrollments[i-1]] = df.iloc[i,2]  
    response = {
        "status": True,
        "enrollments": enrollments,
        "elective_list": elective_list,
        "subject_name_mapping": subject_name_mapping,
        "enrollment_name_mapping": enrollment_name_mapping
    }
    return HttpResponse(json.dumps(response),content_type="application/json")
@csrf_exempt 
@jwt_token_required
def check_result(request):
    
    
    course , passing = json.loads(request.body)['course'] , json.loads(request.body)['passing']
    course = Course.objects.get(id=course)
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

@csrf_exempt 
@jwt_token_required
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
@jwt_token_required
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
@jwt_token_required
def format1(request):
    if request.method=="GET":
        semester = request.GET.get("semester")
        course = request.GET.get("course")
        course_model = Course.objects.get(id=course)
        all_subjects = Subject.objects.filter(course=course_model,semester=semester)
        
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
            course = entry['course']
            course_model = Course.objects.get(id=course)
            result_json = Result.objects.get(course=course_model,passout_year=entry['passing'],semester=entry['semester']).result_json
            result_name = Result.objects.get(course=course_model,passout_year=entry['passing'],semester=entry['semester']).xlsx_file.name
            result_df = pd.read_json(result_json)
            print("result df from the view file \n",result_df)
            try:
                all_subjects_objects = Subject.objects.filter(course=course_model,semester=entry['semester'])
            except Subject.DoesNotExist:
                return HttpResponse("no result found",status=404)
            semester = entry['semester']
            year = entry['passing']
            all_subjects.update({subject.code:subject.subject for subject in all_subjects_objects})
            file_data[result_name] = {
                "result_df": result_df,
                "all_columns": [subject.code for subject in all_subjects_objects],
                "section-subject": entry['section-subject'],
                "course": course_model.abbreviation,
            }
            faculty_name = entry['faculty_name']
            shift = course_model.shift
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
@jwt_token_required
def format2(request):
    if request.method == "POST":
        data = request.body
        data = json.loads(data)
        subject_teacher_mapping = data['subjectTeacherMapping']
        
        faculty_name = data['faculty_name']
        semester = data['semester']
        course = data['course']
        section = data['section']
        batch = data['batch']
        passout_year = data['passing']
        if(int(semester)%2==0):
            month="Jan-July"
        else:
            month="Aug-Dec"
        try:
            course = Course.objects.get(id=course)
            shift = course.shift
            all_subjects = Subject.objects.filter(course=course,semester=semester)
            all_subjects = {subject.code:subject.subject for subject in all_subjects}
            xlsxfile_name = Result.objects.get(course=course,passout_year=passout_year,semester=semester).xlsx_file.name
            json_data = Result.objects.get(course=course,passout_year=passout_year,semester=semester).result_json
            result_df = pd.read_json(json_data)
        except Exception as e:
            return HttpResponse(f"Something went wrong {e}", status=500)
        subject_codes = list(all_subjects.keys())
        format2 = Format_2(result_df,all_subjects,course,semester,shift,section,batch,passout_year,faculty_name,month)
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
@jwt_token_required
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
    main_shift=""
    for i,key in enumerate(keysofdata):
        semester,course=key.split('_')
        faculty_name=data[key]['faculty_name']
        print(data[key]['passing'])
        if(int(semester)%2==0):
            month="Jan-July"
        else:
            month="Aug-Dec"
        all_semesters.append(semester)
        
        admitted_years.append(data[key]['admitted'])
        
        try:
            course=Course.objects.get(id=course)
            Resultobject=Result.objects.get(course=course,passout_year=data[key]['passing'],semester=semester)
            print(Resultobject)
            result_json=Resultobject.result_json
            result_df=pd.read_json(result_json)
        except Exception as e:
            return HttpResponse(f"Something went wrong {e}", status=500)
        
        try:
            all_subjects=Subject.objects.filter(course=course,semester=semester)
        except Exception as e:
            return HttpResponse(f"Something went wrong {e}", status=500)
    
        valuedict['subjects']=[subject.code for subject in all_subjects]
        
        valuedict['needed_subjects']=data[key]['needed_subjects']
        
        valuedict['sections']=data[key]['sections']
        valuedict['course']=course
        all_courses.append(course.abbreviation)
        
        valuedict['shift']=course.shift
        main_shift = course.shift # not sure about this
        
        valuedict['semester']=semester
        valuedict['result_df']=result_df
        file_data[Resultobject.xlsx_file.name]=valuedict
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
    f6 = Format6(file_data,dict_of_all_subjects,faculty_name=faculty_name,shift=main_shift,course=common_letters_string,month=month,admitted_years=admitted_years,all_semesters=all_semesters)
    file_name =f6.write_to_doc()
    with open(os.path.join(os.path.dirname(__file__), "buffer_files", file_name), "rb") as word:
                data = word.read() 
                response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = f'attachment; filename={smart_str(file_name)}'
    os.remove(os.path.join(os.path.dirname(__file__), "buffer_files", file_name))
    return response
    
    


@csrf_exempt 
@jwt_token_required
def format7(request):
    if request.method == "GET":
        semester = request.GET.get("semester")
        course = request.GET.get("course")
        course = Course.objects.get(id=course)
        all_subjects = Subject.objects.filter(course=course,semester=semester)
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
        course = Course.objects.get(id=course)
        semester = data['semester']
        shift = course.shift
        data['shift'] = shift # adding this here because data is being passed to the format7 class and shift is being is accessed from data
        passout_year = data['passing']
        faculty_name = data['faculty_name']
        admitted = data['admitted']
        xlsxfile_name = Result.objects.get(course=course,passout_year=passout_year,semester=semester).xlsx_file.name
        df_json = Result.objects.get(course=course,passout_year=passout_year,semester=semester).result_json
        resut_df = pd.read_json(df_json)
        try:
            all_subjects = Subject.objects.filter(course=course,semester=semester)
        except Exception as e:
            return HttpResponse(f"Something went wrong {e}", status=500)
        all_subjects_dict = {subject.code:subject.subject for subject in all_subjects}
        format7 = Format7(resut_df,data,faculty_name,all_subjects_dict,admitted)
        file_name = format7.write_to_doc()
        with open(os.path.join(os.path.dirname(__file__), "buffer_files", file_name), "rb") as word:
            data = word.read() 
            response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={smart_str(file_name)}'
        os.remove(os.path.join(os.path.dirname(__file__), "buffer_files", file_name))
        return response

@csrf_exempt 
@jwt_token_required  
def getallsubjects(request):
    all_subjects=Subject.objects.all()
    
    all_subjects_list=[]
    for subject in all_subjects:
        subject_dict={}
        subject_dict['course']=subject.course.id
        subject_dict['subject']=subject.subject
        subject_dict['code']=subject.code
        subject_dict['credit']=subject.credit
        subject_dict['is_not_university']=subject.is_not_university
        subject_dict['semester']=subject.semester
        subject_dict['is_practical']=subject.is_practical
        all_subjects_list.append(subject_dict)
        
    return HttpResponse(json.dumps(all_subjects_list),content_type="application/json")
        
@csrf_exempt 
@jwt_token_required        
def getallcourses(request):
    all_courses=Course.objects.all()
    all_courses_list=[]
    
    for course in all_courses:
        course_dict={}
        course_dict['pk']=course.id
        course_dict['name']=course.name
        course_dict['description']=course.description
        course_dict['no_of_semesters']=course.no_of_semesters
        course_dict['abbreviation']=course.abbreviation
        course_dict['shift']=course.shift
        all_courses_list.append(course_dict)
    return HttpResponse(json.dumps(all_courses_list),content_type="application/json")

   
    
    
@csrf_exempt
@jwt_token_required
def student_data(request):
    if request.method == "GET":
        action = request.GET.get("action")
        if action == None:
            response = HttpResponse(json.dumps("NONE Please provide a valid get argument: 'action=template': to fetch the blank csv file , 'action=fetch,course,passout': to fetch data of students of a course 'action=fetch_file,course,passout': to fetch data of students of a course in file format"), status=400)
            return response
        if action.lower() == "template":
            with open(os.path.join(os.path.dirname(__file__), "static", "student data template.csv"), "r") as file:
                data = file.read()
                response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = f'attachment; filename={smart_str("student_data_template.csv")}'
            return response
        elif action.lower() == "fetch":
            course = request.GET.get("course")
            passout = request.GET.get("passout")
            try:
                course = Course.objects.get(id=course)
                student_data = StudentData.objects.get(course=course,passout_year=passout)
                students_info = student_data.students_info_json
                dropped_students = student_data.dropped_sudents_json
                response = HttpResponse(json.dumps({"student_info": json.loads(students_info), "dropped_students":json.loads(dropped_students) }), content_type='application/json')
                return response
            except StudentData.DoesNotExist:
                return HttpResponse("no result found",status=404)
        elif action.lower() == "fetch_file":
            course = request.GET.get("course")
            passout = request.GET.get("passout")
            try:
                course = Course.objects.get(id=course)
                student_data = StudentData.objects.get(course=course,passout_year=passout)
                students_info = student_data.students_info_json
                dropped_students = student_data.dropped_sudents_json
                csv_file = pd.read_json(students_info).to_csv(index=False)
                response = HttpResponse(csv_file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = f'attachment; filename={smart_str("student_data.csv")}'
                return response
            except StudentData.DoesNotExist:
                return HttpResponse("no result found",status=404)
        else:
            response = HttpResponse(json.dumps("NONE Please provide a valid get argument: 'action=template': to fetch the blank csv file , 'action=fetch,course,passout': to fetch data of students of a course 'action=fetch_file,course,passout': to fetch data of students of a course in file format"), status=400)
            return response
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        df = pd.read_csv(csv_file,index_col=None)
        df_copy = df.copy()
        enrollment_col =df_copy.iloc[:,1]
        for i in range(len(enrollment_col)): #making enrollment number a 11 digit string
            enrollment_col[i]=f"{int(enrollment_col[i]):011d}"
        df.iloc[:,1] = enrollment_col
        student_data_json = df.iloc[:, : 4].to_json()
        dropped_students = request.POST.get("dropped_students")
        dropped_students = json.dumps(dropped_students)
        course = request.POST.get("course")
        passout = request.POST.get("passout")
        try:
            course = Course.objects.get(id=course)
            student_data = StudentData.objects.get(course=course,passout_year=passout)
            student_data.students_info_json = student_data_json
            student_data.dropped_sudents_json = dropped_students
            student_data.save()
        except StudentData.DoesNotExist:
            student_data = StudentData.objects.create(course=course,passout_year=passout,students_info_json=student_data_json,dropped_sudents_json=dropped_students)
        return HttpResponse("Data saved successfully")

@csrf_exempt
@jwt_token_required
def delete_student_data(request):
    if request.method == "POST":
        course = request.POST.get("course")
        passout = request.POST.get("passout")
        try:
            course = Course.objects.get(id=course)
            student_data = StudentData.objects.get(course=course,passout_year=passout)
            student_data.delete()
        except StudentData.DoesNotExist:
            return HttpResponse("no result found",status=404)
        return HttpResponse("Data deleted successfully")
    else:
        return HttpResponse("Invalid Request",status=400)
    
    
@csrf_exempt
@jwt_token_required
def check_student_data(request):
    course = request.GET.get("course")
    passout = request.GET.get("passout")
    try:
        course = Course.objects.get(id=course)
        student_data = StudentData.objects.get(course=course,passout_year=passout)
    except StudentData.DoesNotExist:
        return HttpResponse(json.dumps({"status": False}))
    return HttpResponse(json.dumps({"status": True}))
    
@csrf_exempt 
@jwt_token_required
def format11(request):
    if request.method=="GET":
        semester = request.GET.get("semester")
        course = request.GET.get("course")
        course_model = Course.objects.get(id=course)
        all_subjects = Subject.objects.filter(course=course_model,semester=semester)
        
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
            course = entry['course']
            course_model = Course.objects.get(id=course)
            result_json = Result.objects.get(course=course_model,passout_year=entry['passing'],semester=entry['semester']).result_json
            result_name = Result.objects.get(course=course_model,passout_year=entry['passing'],semester=entry['semester']).xlsx_file.name
            result_df = pd.read_json(result_json)
            try:
                all_subjects_objects = Subject.objects.filter(course=course_model,semester=entry['semester'])
            except Subject.DoesNotExist:
                return HttpResponse("no result found",status=404)
            semester = entry['semester']
            year = entry['passing']
            all_subjects.update({subject.code:subject.subject for subject in all_subjects_objects})
            file_data[result_name] = {
                "result_df": result_df,
                "all_columns": [subject.code for subject in all_subjects_objects],
                "section-subject": entry['section-subject'],
                "course": course_model.abbreviation,
            }
            faculty_name = entry['faculty_name']
            shift = course_model.shift
        practical_subjects = [subject.code for subject in all_subjects_objects if subject.is_practical]
        
        format11 = f11(file_data=file_data,all_subjects=all_subjects,faculty_name=faculty_name,shift=shift,semester=semester,passing=year , practical_subjects=practical_subjects)
        file_name = format11.write_to_doc()
        file_path = os.path.join(os.path.dirname(__file__), "buffer_files", file_name)
        with open(file_path, "rb") as word:
            data = word.read()
            response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={smart_str(file_name)}'
        os.remove(os.path.join(os.path.dirname(__file__), "buffer_files", file_name))
        return response
 
 
 #data i will get for format 4 to process further 

@csrf_exempt 
@jwt_token_required 
def format4(request):
    reqbody=request.body
    reqdata=json.loads(reqbody)
    file_data=[]
    filedatadict={}
    for i in reqdata:
        print("i",i)
        valuedict={}
        
        course=Course.objects.get(id=i['course'])
        valuedict['course']=course.abbreviation
        valuedict['shift']=course.shift 
        for year in i['data']:
            print("year",year)
            try:
                yeardictdata={}
                semesterdictdata={}
                
                results=Result.objects.filter(course=course,passout_year=year)
                for result in results:
                    result_json=result.result_json
                    result_df=pd.read_json(result_json)
                    # result_df=result_json
                    sem=result.semester
                    semesterdictdata[sem]=result_df
                finalyear=f'{int(year)-(course.no_of_semesters//2)}-{str(year)}'
                yeardictdata[finalyear]=semesterdictdata
                print("year d data",yeardictdata)
                if "data" not in valuedict.keys():
                    valuedict['data']={}
                for key,value in yeardictdata.items():
                    valuedict['data'][key]=value
                print("valuedict",valuedict)
            except Exception as e:
                return HttpResponse(f"Something went wrong {e}", status=500)
        file_data.append(valuedict)
    print(file_data)
    # return HttpResponse(json.dumps(file_data),content_type="application/json")
    format4=f4(file_data)
    file_name = format4.write_to_doc()
    file_path = os.path.join(os.path.dirname(__file__), "buffer_files", file_name)
    with open(file_path, "rb") as word:
        data = word.read()
        response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={smart_str(file_name)}'
    os.remove(os.path.join(os.path.dirname(__file__), "buffer_files", file_name))
    return response
        
@csrf_exempt 
@jwt_token_required
def format5(request): 
    reqbody=request.body
    reqdata=json.loads(reqbody)  
    course=Course.objects.get(id=reqdata['course'])
    student_data = StudentData.objects.get(course=course,passout_year=reqdata['passout_year'])
    students_info = pd.read_json(student_data.students_info_json)
    results=Result.objects.filter(course=course,passout_year=reqdata['passout_year'])
    data={}
    data["student-data"]=students_info
    for result in results:
        result_json=result.result_json
        result_df=pd.read_json(result_json)
        sem=result.semester
        data[sem]=result_df
    reqdata['data']=data
    reqdata['course']=course.abbreviation
    reqdata['shift']=course.shift
    format5=f5(reqdata)
    file_name = format5.format()
    file_path = os.path.join(os.path.dirname(__file__), "buffer_files", file_name)
    with open(file_path, "rb") as word:
        data = word.read()
        response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={smart_str(file_name)}'
    os.remove(os.path.join(os.path.dirname(__file__), "buffer_files", file_name))
    return response
    
    
    
            
            
                    
                   