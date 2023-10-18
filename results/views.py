from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from .one import One
@csrf_exempt
def normalize(request):
    print(request)
    print(request.FILES)
    one = One(request.FILES.get("pdf"))
    print(one)
    
    normalized_pdf = one.normalize()
    print(normalized_pdf)
    return HttpResponse(normalized_pdf, content_type='application/pdf')
    

    