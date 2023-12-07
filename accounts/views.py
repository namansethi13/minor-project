from django.shortcuts import render , HttpResponse
# allowed method decorator
from django.contrib.auth import login as auth_login , authenticate , logout as auth_logout
from django.utils import timezone
from django.views.decorators.http import require_http_methods 
import random
import json
from  .models import customUser
from .send_email import send_email

from django.shortcuts import redirect

def login_teacher(request):
    if request.method == "POST":
        email = request.POST["email"]
        OTP = request.POST["OTP"]
        #if email exists in database
        if customUser.objects.filter(email=email).exists():
            user_teacher = customUser.objects.get(email=email)
            if user_teacher.otp_valid_till > timezone.now():
                if user_teacher.otp == OTP:
                    user_t = authenticate(request, username=user_teacher.email, password="password")
                    print("this is the authenticated user",user_t)
                    if user_t is not None:
                        auth_login(request, user_t)
                        return redirect("/results/convert/")
                    else:
                        print("user is none")
                    user_teacher.otp_valid_till =  user_teacher.otp_valid_till - timezone.timedelta(minutes=15)
                    user_teacher.save()
                    print("login success")
                # HttpResponse(json.dumps({"status":"true","otp": num})
                else:
                    return HttpResponse("OTP is wrong" , status=400) 

            else:
                return HttpResponse("OTP is expired", status=400)
        else:
            return HttpResponse("User does not exists", status=404)
        print(user_teacher.email, OTP)

    
    return render(request, "login.html")

@require_http_methods(["POST"])
def send_otp(request):
    # print(request.POST)
    num = random.randint(1000, 9999)
    data = json.loads(request.body.decode('utf-8'))
    
    # Now you can access the 'email' key from the data dictionary
    email = data.get('email')
    if "@msijanakpuri.com" not in email or len(email) == len("@msijanakpuri.com"):
        return  HttpResponse(json.dumps({"status": "false", "error": "@msijanakpuri mail is required"}), content_type="application/json")
    if customUser.objects.filter(email=email).exists():
        user = customUser.objects.get(email=email)
        if user.otp_valid_till is not None:
            if user.otp_valid_till > timezone.now():
                print("OTP already sent")
                return  HttpResponse(json.dumps({"status": "false", "error": "OTP is already sent"}), content_type="application/json")
        user.otp = num
        user.otp_valid_till = timezone.now() + timezone.timedelta(minutes=5)
        user.save()
        send_email(num , email)
        print("OTP sent")
        return  HttpResponse(json.dumps({"status":"true"}), content_type="application/json")
    return HttpResponse(json.dumps({"status": "false", "error": "User does not exists"}), content_type="application/json", status=404)
    

def logout(request):
    auth_logout(request)
    return redirect("/accounts/login_teacher/")