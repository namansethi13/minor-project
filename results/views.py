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
        subject_name_mapping = {'020102(4)': '020102 Applied Maths (Internal)',
                            '020102(4).1': '020102 Applied Maths (External)',
                            '020102(4).2': '020102 Applied Maths (Total)',
                            '020104(4)': '020104 Web Based Programming (Internal)',
                            '020104(4).1': '020104 Web Based Programming (External)',
                            '020104(4).2': '020104 Web Based Programming (Total)',
                            '020106(4)': '020106 Data Structures & Algorithm Using C (Internal)',
                            '020106(4).1': '020106 Data Structures & Algorithm Using C (External)',
                            '020106(4).2': '020106 Data Structures & Algorithm Using C (Total)',
                            '020108(4)': '020108 DBMS (Internal)',
                            '020108(4).1': '020108 DBMS (External)',
                            '020108(4).2': '020108 DBMS (Total)',
                            '020110(2)': '020110 EVS (Internal)',
                            '020110(2).1': '020110 EVS (External)',
                            '020110(2).2': '020110 EVS (Total)',
                            '020136(2)': '020136 SAUE (Internal)',
                            '020136(2).1': '020136 SAUE (External)',
                            '020136(2).2': '020136 SAUE (Total)',
                            '020172(2)': '020172 Practical IV-WBP Lab (Internal)',
                            '020172(2).1': '020172 Practical IV-WBP Lab (External)',
                            '020172(2).2': '020172 Practical IV-WBP Lab (Total)',
                            '020174(2)': '020174 Practical- V DS Lab (Internal)',
                            '020174(2).1': '020174 Practical- V DS Lab (External)',
                            '020174(2).2': '020174 Practical- V DS Lab (Total)',
                            '020176(2)': '020176 Practical- VI DBMS Lab (Internal)',
                            '020176(2).1': '020176 Practical- VI DBMS Lab (External)',
                            '020176(2).2': '020176 Practical- VI DBMS Lab (Total)',
                            }
        headers_to_add = [["Maharaja Surajmal Institute"],
                      ["BCA(M) Batch 2022-2025"],
                      ["Class-: BCA  II Semester Batch [2022-2025]     Jan- June 2023"],
                      ]
        footers_to_add = [["102-Applied Maths Dr. Anchal Tehlan (Sec A & B)"],
                      ["104-WBP - Mr. Sundeep Kumar(A) & Ms. Kanika Kundu (B)"],
                      ["106-Data Struc Using C - Dr.Neetu Anand(A )   Mr.Manoj Kumar (B )"],
                      ["108-DBMS - Ms.Kanika Kundu (A) & Ms.Vinita Tomar(B)"],
                      ["110-EVS - Dr.Manju Dhillon (Sec A & Sec B)"],
                      ["172-WBP Lab - Mr.Sundeep Kumar/ Dr.Neetu Narwal (Sec A) &  Ms.Kanika Kundu(Sec A) & Dr.Neetu Narwal (Sec B)"],
                      ["174- DS Lab - Dr.Neetu Anand /Dr.Kumar Gaurav (A ) &  Mr.Manoj Kumar (B )"],
                      ["176- DBMS Lab - Ms.Kanika Kundu / Mr. Siddharth Shankar (A)   &  Ms.Vinita Tomar (B)"],
                      [""],
                      ["Class Coordinator: Ms.Anchal Tehlan (Sec A) - Mr.Manoj Kumar (Sec B)"],
                      ]
        exclude_subject_code = "20136"
        processor = ResultProcessor(request.FILES.get("pdf"),'output.xlsx', subject_name_mapping, exclude_subject_code,footers_to_add , headers_to_add)
        
        return HttpResponse(one, content_type='application/pdf')    


        # one=one.convert()
        #converter.convert()
    except Exception as e:
        print(e)
    
    print(one)
    

@login_required
def convert(request):
    return render(request, 'convert.html')
    

    