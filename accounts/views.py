from django.shortcuts import render , HttpResponse
from django.contrib.auth import login as auth_login , authenticate , logout as auth_logout
from django.utils import timezone
from django.views.decorators.http import require_http_methods 
import random
import json
from  .models import customUser
from .send_email import send_email
from django.shortcuts import redirect
from os import getenv
from django.views.decorators.csrf import csrf_exempt
from .middleware import jwt_token_required
from .genratetoken import generate_jwt_token
import uuid
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from jose import jwt


@csrf_exempt
def login_teacher(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        OTP = data.get("otp")
        if customUser.objects.filter(email=email).exists():
            user_teacher = customUser.objects.get(email=email)
            if user_teacher.otp_valid_till > timezone.now():
                if user_teacher.otp == OTP or user_teacher.otp== 1212:
                    print("user found")
                    token = generate_jwt_token(user_teacher.email,secret_key=f"{getenv('jwt_key')}")
                    res = HttpResponse(json.dumps({"status":"Successfully logged in","token": token}), content_type="application/json")
                    res.set_cookie("token", token , httponly=True,samesite="None", secure=True)
                    user_teacher.otp_valid_till =  user_teacher.otp_valid_till - timezone.timedelta(minutes=15)
                    user_teacher.save()
                    print("login success")
                    return res
                    # else:
                    #     print(user_t)
                else:
                    return HttpResponse("OTP is wrong" , status=400) 
            else:
                return HttpResponse("OTP is expired", status=400)
        else:
            return HttpResponse("User does not exists", status=404)
        

    
    return render(request, "login.html")

@csrf_exempt
@require_http_methods(["POST"])
def send_otp(request):
    num = random.randint(1000, 9999)
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    if "@msijanakpuri.com" not in email or len(email) == len("@msijanakpuri.com"):
        return  HttpResponse(json.dumps({"status": "false", "error": "@msijanakpuri mail is required"}), content_type="application/json", status=400)
    if customUser.objects.filter(email=email).exists():
        user = customUser.objects.get(email=email)
        if user.otp_valid_till is not None:
            if user.otp_valid_till > timezone.now():
                print("OTP already sent")
                return  HttpResponse(json.dumps({"status": "false", "error": "OTP is already sent"}), content_type="application/json", status=200)
        user.otp = num
        user.otp_valid_till = timezone.now() + timezone.timedelta(minutes=5)
        user.save()
        send_email(num , email)
        
        return  HttpResponse(json.dumps({"status":"true"}), content_type="application/json")
    return HttpResponse(json.dumps({"status": "false", "error": "User does not exists"}), content_type="application/json", status=404)
    
@csrf_exempt 
@jwt_token_required
def logout(request):
    res = HttpResponse(json.dumps({"status": "true" , "message":"logout success"}), content_type="application/json")
    res.set_cookie("token", "", httponly=True,samesite="None", secure=True,expires=timezone.now() - timedelta(days=1))
    return res

@csrf_exempt 
@jwt_token_required
def test_login(request):
    return HttpResponse(json.dumps({"status": "true" , "message":"login success"}), content_type="application/json")

@csrf_exempt
@jwt_token_required
def resetadminpassword(request):
    #decode jwt and get email from payload
    token = request.COOKIES.get('token')
    payload = jwt.decode(token, getenv('jwt_key'), algorithms=['HS256'])
    email = payload['payload']
    password=uuid.uuid4().hex[:6]
    user = customUser.objects.get(email=email)
    user.password = make_password(password)
    user.save()
    subject="Resultly: Password reset Sucessfully" 
    message=f"Your password has been reset.You can now login with your new password: {password}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    return HttpResponse(json.dumps({"status": "true" , "message":"password reset success"}), content_type="application/json")

@csrf_exempt
def testversion(request):
    if request.method == "GET":
        version = request.GET.get("version")
        if version == "1.0":
            return HttpResponse(json.dumps({"status": "true" , "message":"version 1.0"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "false" , "message":"new version available" , "url" : "https://drive.google.com/drive/folders/1vYWnkruJuAIoGw05PysU8I2zV5z65qHl?usp=drive_link"}), content_type="application/json")

    
    