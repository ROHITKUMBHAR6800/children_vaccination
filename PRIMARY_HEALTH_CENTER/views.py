from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from random import randint
from django.core.mail import send_mail
import PRIMARY_HEALTH_CENTER
from PRIMARY_HEALTH_CENTER.models import *
from django.db.models import Q
from smtplib import SMTPException, SMTPRecipientsRefused
from CHILD_VACCINATION import settings
from PRIMARY_HEALTH_CENTER.tasks import insertIntoChildVaccModel,send_updates

# Create your views here.

def otp():
    otp=str(randint(100000,999999))
    return otp


def password_gen():
    ps="@"
    for i in range(2):
        ch=randint(65,90)
        ps+=chr(ch)
    for i in range(2):
        ch=randint(97,122)
        ps+=chr(ch)
    for i in range(3):
        num=randint(0,9)
        ps+=str(num)
    return ps


# otp will be send by using folling the function and if there any invalid email address then expect block will run
def send_otp(mail,otp):
    subject = "OTP"
    message = f"This is system generated mail please do not reply and share mail with anyone. This is your {otp}"
    sender = settings.EMAIL_HOST_USER
    receiver = [mail]
    try:
        send_mail(subject, message, sender, receiver)
        return True
    except(SMTPException, SMTPRecipientsRefused):
        return False
      

def homePage(request):
    return render(request, 'homepage.html')

def contactUsPage(request):
    return render(request, 'contactUs.html')

def aboutUsPage(request):
    return render(request, 'aboutUs.html')

def adminLoginForm(request):
    return render(request, 'adminLoginForm.html')

def adminRegistrationForm(request):
    return render(request, 'adminRegistrationForm.html')

def forgetPasswordForm(request):
    return render(request, 'forpwdForm.html')

def userLoginForm(request):
    return render(request, 'userLoginForm.html')



def admin_registration(request):
    if request.method == 'POST':
        mail=request.POST.get("email")
        if len(Admin.objects.filter(email=mail))>0:
            return JsonResponse("email id or user exist already",safe=False)
        
        ot = otp()
        output = send_otp(mail,ot)
        if output == False:
            return JsonResponse("invalid email id",safe = False)

        password=request.POST.get("password")
        confirm_password=request.POST.get("confirmPassword")
        if password!=confirm_password:
            return JsonResponse("both password are different",safe=False)
        
        adminRefVar=Admin(hospital_name=request.POST.get("hospitalName"),
                        mobile_no=request.POST.get("mobileNo"),
                        email=mail,
                        state=request.POST.get("state"),
                        district=request.POST.get("district"),
                        tehsil=request.POST.get("tehsil"),
                        village_town=request.POST.get("villageTown"),
                        area_add=request.POST.get("areaAdd"),
                        pincode=request.POST.get("pincode"),
                        password=password,
                        otp=ot
                        )
        adminRefVar.save()
        return render(request,'emailVerify.html')
    else:
        return JsonResponse("invalid method",safe = False)
    

def user_registration(request):
    if request.method == 'POST':
        mail=request.POST.get("email")
        if len(Users.objects.filter(email=mail))>0:
            return JsonResponse("user with email id exist already",safe=False)
        
        ot = otp()
        output = send_otp(mail,ot)
        if output == False:
            return JsonResponse("invalid email id",safe = False)

        password=request.POST.get("password")
        confirm_password=request.POST.get("confirmPassword")
        if password!=confirm_password:
            return JsonResponse("both password are different",safe=False)
        
        adminId=request.POST.get("adminId")
        pwd=request.POST.get("adminPassword")
        try:
            Admin.objects.get(admin_id=adminId,password=pwd)
        except PRIMARY_HEALTH_CENTER.models.Admin.DoesNotExist:
            return JsonResponse("invalid amdin id or password", safe=False)
        
        usersRefVar=Users(admin_id=adminId,
                        user_name=request.POST.get("firstName"),
                        middle_name=request.POST.get("middleName"),
                        surname=request.POST.get("surname"),
                        gender=request.POST.get("gender"),
                        mobile_no=request.POST.get("mobileNo"),
                        email=mail,
                        state=request.POST.get("state"),
                        district=request.POST.get("district"),
                        tehsil=request.POST.get("tehsil"),
                        village=request.POST.get("villageTown"),
                        home_add=request.POST.get("areaAdd"),
                        pincode=request.POST.get("pincode"),
                        password=password,
                        otp=ot
                        )
        usersRefVar.save()
        return render(request,'emailVerify.html')
    else:
        return JsonResponse("invalid method",safe = False)
    

def child_registration(request):
    if request.method == 'POST':
        bcid=request.POST.get("birthCertificateId")
        childId="ch00-"+bcid
        if len(Child.objects.filter(child_id=childId))>0:
            return JsonResponse("child registered already",safe=False)
        
        birth_date=request.POST.get("birthDate") 
        mail=request.POST.get("email")

        ot = otp()
        output = send_otp(mail,ot)
        if output == False:
            return JsonResponse("invalid email id",safe = False)
        
        registerBy=request.POST.get("registerBy")
        pwd=request.POST.get("password")
        try:
            Users.objects.get(user_id=registerBy,password=pwd)
        except PRIMARY_HEALTH_CENTER.models.Users.DoesNotExist:
            try:
                Admin.objects.get(admin_id=registerBy,password=pwd)
            except PRIMARY_HEALTH_CENTER.models.Admin.DoesNotExist:
                return JsonResponse("invalid id or password", safe=False)

        childRefVar=Child(child_id=childId,
                        register_by=registerBy,
                        child_name=request.POST.get("childName"),
                        father_name=request.POST.get("fatherName"),
                        surname=request.POST.get("surname"),
                        mother_name=request.POST.get("motherName"),
                        birth_date=birth_date,
                        gender=request.POST.get("gender"),
                        mobile_no=request.POST.get("mobileNo"),
                        email=mail,
                        state=request.POST.get("state"),
                        district=request.POST.get("district"),
                        tehsil=request.POST.get("tehsil"),
                        village=request.POST.get("villageTown"),
                        home_add=request.POST.get("areaAdd"),
                        pincode=request.POST.get("pincode"),
                        otp=ot
                        )
        childRefVar.save()
        
        insertIntoChildVaccModel.delay(childId,mail,birth_date)

        return render(request,'emailVerify.html')
    
    else:
        return JsonResponse("invalid method",safe = False)

def verify_email(request):
    if request.method == 'POST':
        mail = request.POST.get("email")
        ot = request.POST.get("otp")
        try:
            data=Child.objects.get(email=mail,email_verify="unverified")
            if data.otp==ot:
                data.email_verify = 'verified'
                data.save()
                sub="REGISTRATION SUCCESSFUL"
                mes =f"You are registered successfully and your id is {data.child_id}."
                send_updates(mail,sub,mes)
                return JsonResponse("Your registration is successfull",safe=False)
            else:
                return JsonResponse("invalid otp",safe=False)
        except PRIMARY_HEALTH_CENTER.models.Child.DoesNotExist:
            try:
                data=Users.objects.get(email=mail,email_verify="unverified")
                if data.otp==ot:
                    data.email_verify = 'verified'
                    data.save()
                    sub="REGISTRATION SUCCESSFUL"
                    mes =f"You are registered successfully and your id is {data.user_id}. Please do not share your id and password to anyone."
                    send_updates(mail,sub,mes)
                    return JsonResponse("Your registration is successfull",safe=False)
                else:
                    return JsonResponse("invalid otp",safe=False)
            except PRIMARY_HEALTH_CENTER.models.Users.DoesNotExist:
                try:
                    data=Admin.objects.get(email=mail,email_verify="unverified")
                    if data.otp==ot:
                        data.email_verify = 'verified'
                        data.save()
                        sub="REGISTRATION SUCCESSFUL"
                        mes =f"You are registered successfully and your id is {data.admin_id}. Please do not share your id and password to anyone."
                        send_updates(mail,sub,mes)
                        return JsonResponse("Your registration is successfull",safe=False)
                    else:
                        return JsonResponse("invalid otp",safe=False)
                except PRIMARY_HEALTH_CENTER.models.Admin.DoesNotExist:
                    return JsonResponse("invalid email", safe=False)
    else:
        return JsonResponse("invalid method",safe = False)  


def update_child(request):
    if request.method == 'POST':
        registerById=request.POST.get("registerById")
        pwd=request.POST.get("password")
        try:
            Users.objects.get(user_id=registerById,password=pwd)
        except PRIMARY_HEALTH_CENTER.models.Users.DoesNotExist:
            try:
                Admin.objects.get(admin_id=registerById,password=pwd)
            except PRIMARY_HEALTH_CENTER.models.Admin.DoesNotExist:
                return JsonResponse("invalid id or password", safe=False)
        childId=request.POST.get('childId')
        mail=request.POST.get("email")
        try:
            data=Child.objects.get(child_id=childId,email=mail)
            data.register_by=registerById
            data.child_name=request.POST.get("childName")
            data.mobile_no=request.POST.get("mobileNo")
            data.state=request.POST.get("state")
            data.district=request.POST.get("district")
            data.tehsil=request.POST.get("tehsil")
            data.village=request.POST.get("villageTown")
            data.home_add=request.POST.get("areaAdd")
            data.pincode=request.POST.get("pincode")
            data.save()

            sub="CREDINTAILS UPDATED SUCCESSFULLY"
            mes ="Your credintials updated successfully."
            send_updates(mail,sub,mes)

            return JsonResponse('Child credentials updated succefully',safe=False)
        except PRIMARY_HEALTH_CENTER.models.Child.DoesNotExist:
                return JsonResponse("invalid Child Id or email id", safe=False)
    else:
        return JsonResponse("invalid method",safe = False)


def delete_user(request):
    if request.method == 'POST':
        adminId=request.POST.get('adminId')
        pwd=request.POST.get('password')
        userId=request.POST.get('userId')
        mail=request.POST.get('email')
        try:
            Admin.objects.get(admin_id=adminId,password=pwd)
            try:
                data=Users.objects.get(user_id=userId,email=mail)
                data.delete()
                sub="CREDINTAILS DELETED BY ADMIN"
                mes ="Your credintials deleted by admin, you are not longer participant."
                send_updates(mail,sub,mes)
                return JsonResponse('user deleted succefully',safe=False)
            except PRIMARY_HEALTH_CENTER.models.Users.DoesNotExist:
                return JsonResponse("invalid user id or email", safe=False)
        except PRIMARY_HEALTH_CENTER.models.Admin.DoesNotExist:
                return JsonResponse("invalid admin id or password", safe=False)
    else:
        return JsonResponse("invalid method",safe = False)
        
    
def delete_child(request):
    if request.method == 'POST':
        adminId=request.POST.get('adminId')
        pwd=request.POST.get('password')
        registerById=request.POST.get('registerById')
        childId=request.POST.get("childId")
        try:
            Admin.objects.get(admin_id=adminId,password=pwd)
            try:
                data=Child.objects.get(child_id=childId,register_by=registerById)
                mail=data.email
                data.delete()
                sub="CREDINTAILS DELETED BY ADMIN"
                mes ="Your credintials deleted by admin, you are not longer participant."
                send_updates(mail,sub,mes)
                return JsonResponse('Child credentials deleted succefully',safe=False)
            except PRIMARY_HEALTH_CENTER.models.Child.DoesNotExist:
                return JsonResponse("invalid registerby id or Child Id", safe=False)
        except PRIMARY_HEALTH_CENTER.models.Admin.DoesNotExist:
                return JsonResponse("invalid admin id or password", safe=False)
    else:
        return JsonResponse("invalid method",safe = False)


def forgot_password(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        try:
            data=Users.objects.get(user_id=id)
            pwd=password_gen()
            data.password=pwd
            data.save()
            sub="NEW PASSWORD"
            mes =f"Your new password is {pwd}. Please do not share your id and password to anyone."
            send_updates(data.email,sub,mes)
            return render(request,'testpage.html')
        except PRIMARY_HEALTH_CENTER.models.Users.DoesNotExist:
            try:
                data=Admin.objects.get(admin_id=id)
                pwd=password_gen()
                data.password=pwd
                data.save()
                sub="NEW PASSWORD"
                mes =f"Your new password is {pwd}. Please do not share your id and password to anyone."
                send_updates(data.email,sub,mes)
                return render(request,'testpage.html')
            except PRIMARY_HEALTH_CENTER.models.Admin.DoesNotExist:
                return HttpResponse('invalid credentials')
    else:
        return JsonResponse("invalid method",safe = False)
        
        
def change_password(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        oldpwd=request.POST.get('oldPassword')
        newpwd=request.POST.get('newPassword') 
        try:
            data=Users.objects.get(user_id=id,password=oldpwd)
            data.password=newpwd
            data.save()
            return JsonResponse('your password changed succefully',safe=False)
        except PRIMARY_HEALTH_CENTER.models.Users.DoesNotExist:
            try:
                data=Admin.objects.get(admin_id=id,password=oldpwd)
                data.password=newpwd
                data.save()
                return JsonResponse('your password changed succefully',safe=False)
            except PRIMARY_HEALTH_CENTER.models.Admin.DoesNotExist:
                return JsonResponse("invalid id or old password", safe=False)
    else:
        return JsonResponse("invalid method",safe = False)


def admin_page(request):
    if request.method != "POST":
        return JsonResponse("invalid method",safe=False)
    id = request.POST.get("adminId")
    pwd = request.POST.get("password")
    
    