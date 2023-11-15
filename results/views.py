from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse


from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
subject_codes_dict = {
    'BCA202': 'Java',
    'BCA204': 'Software Engineering',
    'BCA206': 'Entrepreneurship Development',
    'BCA208': 'Django',
    'BCA210': 'Data Science',
    'BCA212': 'Digital Marketing'
}



subject_credits_dict = {
    'Java': 3,
    'Software Engineering': 4,
    'Entrepreneurship Development': 2,
    'Django': 3,
    'Data Science': 3,
    'Digital Marketing': 2
}



from .conversions import ResultProcessor
@csrf_exempt
def normalize(request):
    print(request)
    print(request.FILES)
    try:
        subject_name_mapping = {
        '020102(4)': 'Applied Maths (Internal)',
        '020102(4).1': 'Applied Maths (External)',
        '020102(4).2': 'Applied Maths (Total)',
        '020104(4)': 'Web Based Programming (Internal)',
        '020104(4).1': 'Web Based Programming (External)',
        '020104(4).2': 'Web Based Programming (Total)',
        '020106(4)': 'Data Structures & Algorithm Using C (Internal)',
        '020106(4).1': 'Data Structures & Algorithm Using C (External)',
        '020106(4).2': 'Data Structures & Algorithm Using C (Total)',
        '020108(4)': 'DBMS (Internal)',
        '020108(4).1': 'DBMS (External)',
        '020108(4).2': 'DBMS (Total)',
        '020110(2)': 'EVS (Internal)',
        '020110(2).1': 'EVS (External)',
        '020110(2).2': 'EVS (Total)',
        '020136(2)': 'SAUE (Internal)',
        '020136(2).1': 'SAUE (External)',
        '020136(2).2': 'SAUE (Total)',
        '020172(2)': 'Practical IV-WBP Lab (Internal)',
        '020172(2).1': 'Practical IV-WBP Lab (External)',
        '020172(2).2': 'Practical IV-WBP Lab (Total)',
        '020174(2)': 'Practical- V DS Lab (Internal)',
        '020174(2).1': 'Practical- V DS Lab (External)',
        '020174(2).2': 'Practical- V DS Lab (Total)',
        '020176(2)': 'Practical- VI DBMS Lab (Internal)',
        '020176(2).1': 'Practical- VI DBMS Lab (External)',
        '020176(2).2': 'Practical- VI DBMS Lab (Total)',
    }
        exclude_subject_code = "20136"
        processor = ResultProcessor(request.FILES.get("pdf"),'output.xlsx', subject_name_mapping, exclude_subject_code)
        print("object created")
        processor.read_data()
        print("object created1")
        processor.rename_columns()
        print("object created2")
        processor._calculate_cgpa()
        print("object created3")
        processor.process_absents()
        print("object created4")
        processor.process_reappear()
        print("object created5")
        processor.update_reappear_absent_columns()
        print("object created6")
        one = processor.save_result()
        print(one)
        print("result saved in one")
        return HttpResponse(one, content_type='application/pdf')


        # one=one.convert()
        #converter.convert()
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print(one)
    

@login_required
def convert(request):
    return render(request, 'convert.html')
    

    