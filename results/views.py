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



from .conversions import ExcelToCSVConverter
@csrf_exempt
def normalize(request):
    print(request)
    print(request.FILES)
    
    try:
        one =ExcelToCSVConverter(request.FILES.get("pdf"),'output.csv', subject_codes_dict, subject_credits_dict)
        one=one.convert()
        #converter.convert()
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print(one)
    
    ##normalized_pdf = converter.convert()
    print(one)
    return HttpResponse(one, content_type='application/pdf')

@login_required
def convert(request):
    return render(request, 'results/convert.html')
    

    