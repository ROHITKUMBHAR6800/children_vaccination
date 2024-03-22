from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
from random import randint
from django.http import JsonResponse
from django.core.mail import send_mail
import PRIMARY_HEALTH_CENTER

from PRIMARY_HEALTH_CENTER.models import *
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
from django.db.models import Q


def otp():
    otp=""
    for i in range(4):
        ch=randint(0,9)
        otp+=str(ch)
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


def outputSendMail(emailId,output):
    if len(output)==4 and output.isdigit():
        send_mail("email verification",
                "     This is system generated mail, please don't reply and share anything. This is your otp: "+output,
                "phchol06082001@gmail.com",
                [emailId])
    elif output.startswith('admin00') or output.startswith('user00') or output.startswith('ch00-'):
        send_mail("Your registration is successful",
              "    This is system generated mail, please don't share your id to anyone. It will help to further use over CHILD VACCINATION-IMMUNITION PROGRAMME portal. This is your id: "+output,
              "phchol06082001@gmail.com",
              [emailId])
    elif len(output)==8 and output.startswith('@'):
        send_mail("Forget password",
              "    This is system generated mail, please don't share your password to anyone. It will help to further use over CHILD VACCINATION-IMMUNITION PROGRAMME portal. This is your new password: "+output,
              "phchol06082001@gmail.com",
              [emailId])
    elif output=="update":
        send_mail("Cedentials updated successfully",
              "    This is system generated mail. Your credentials updated successfully on CHILD VACCINATION-IMMUNITION PROGRAMME portal. ",
              "phchol06082001@gmail.com",
              [emailId])
    elif output=="delete":
        send_mail("Remove by ADMIN",
              "    This is system generated mail. From now your are not a part of CHILD VACCINATION-IMMUNITION PROGRAMME portal. Your credentials deleted by 'ADMIN'. ",
              "phchol06082001@gmail.com",
              [emailId])
      

def homepage(request):
    template=loader.get_template('homepage.html')
    return HttpResponse(template.render())

def admin_registration(request):
    mail=request.POST.get("email")
    if len(Admin.objects.filter(email=mail))>0:
        return JsonResponse("email id or user exist already",safe=False)
    
    # otp=otp()
    # outputSendMail(mail,otp)
    # otp=request.POST.get("otp")
    # if otp!=otp:
    #     return JsonResponse("either otp or email id is invalid",safe=False)

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
                    password=password
                    )
    adminRefVar.save()
    data=Admin.objects.get(email=mail)
    outputSendMail(mail,data.admin_id)
    return JsonResponse("profile created successfully",safe=False)


def user_registration(request):
    mail=request.POST.get("email")
    if len(Users.objects.filter(email=mail))>0:
        return JsonResponse("user with email id exist already",safe=False)
    
    # otp=otp()
    # outputSendMail(mail,otp)
    # otp=request.POST.get("otp")
    # if otp!=otp:
    #     return JsonResponse("either otp or email id is invalid",safe=False)

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
                    password=password
                    )
    usersRefVar.save()
    data=Users.objects.get(email=mail)
    outputSendMail(mail,data.user_id)
    return JsonResponse("user profile created successfully",safe=False)


def delete_user(request):
    adminId=request.POST.get('adminId')
    pwd=request.POST.get('password')
    userId=request.POST.get('userId')
    mail=request.POST.get('email')
    try:
        Admin.objects.get(admin_id=adminId,password=pwd)
        try:
            data=Users.objects.get(user_id=userId,email=mail)
            data.delete()
            output="delete"
            outputSendMail(mail,output)
            return JsonResponse('user deleted succefully',safe=False)
        except PRIMARY_HEALTH_CENTER.models.Users.DoesNotExist:
            return JsonResponse("invalid user id or email", safe=False)
    except PRIMARY_HEALTH_CENTER.models.Admin.DoesNotExist:
            return JsonResponse("invalid admin id or password", safe=False)
    

def child_registration(request):
    bcid=request.POST.get("birthCertificateId")
    childId="ch00-"+bcid
    if len(Child.objects.filter(child_id=childId))>0:
        return JsonResponse("child registered already",safe=False)
    
    birth_date=request.POST.get("birthDate") 
    mail=request.POST.get("email")
    # otp=otp()
    # otpSendMail(mail,otp)
    # otp=request.POST.get("otp")
    # if otp!=otp:
    #     return JsonResponse("either otp or email id is invalid", safe=False)
    
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
                    pincode=request.POST.get("pincode")
                    )
    childRefVar.save()
    
    def add_months_to_date(birth_date_str, months_to_add):
        # Example usage:
        # birth_date_str = '2000-01-01'  # Example birth date string
        # months_to_add = 6 
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
        new_date = birth_date + relativedelta(months=months_to_add)
        return new_date.strftime('%Y-%m-%d')
    
    childVaccRefVar=ChildVaccination(child=childRefVar,
                                    email=mail,
                                    vaccination_1month= add_months_to_date(birth_date, 1),
                                    vaccination_2month= add_months_to_date(birth_date, 2),
                                    vaccination_3month= add_months_to_date(birth_date, 3),
                                    vaccination_6month= add_months_to_date(birth_date, 6),
                                    vaccination_7month= add_months_to_date(birth_date, 7),
                                    vaccination_8month= add_months_to_date(birth_date, 8),
                                    vaccination_9month= add_months_to_date(birth_date, 9),
                                    vaccination_12month= add_months_to_date(birth_date, 12),
                                    vaccination_15month= add_months_to_date(birth_date, 15),
                                    vaccination_18month= add_months_to_date(birth_date, 18),
                                    vaccination_24month= add_months_to_date(birth_date, 24),
                                    vaccination_36month= add_months_to_date(birth_date, 36),
                                    vaccination_48month= add_months_to_date(birth_date, 48),
                                    vaccination_60month= add_months_to_date(birth_date, 60)
                                    )
    childVaccRefVar.save()
    outputSendMail(mail,childId)
    return JsonResponse("child profile created successfully",safe=False)


def update_child(request):
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
        output="update"
        outputSendMail(mail,output)
        return JsonResponse('Child credentials updated succefully',safe=False)
    except PRIMARY_HEALTH_CENTER.models.Child.DoesNotExist:
            return JsonResponse("invalid Child Id or email id", safe=False)
    
def delete_child(request):
    adminId=request.POST.get('adminId')
    pwd=request.POST.get('password')
    registerById=request.POST.get('registerById')
    childId=request.POST.get("childId")
    try:
        Admin.objects.get(admin_id=adminId,password=pwd)
        try:
            data=Child.objects.get(child_id=childId,register_by=registerById)
            email=data.email
            data.delete()
            output="delete"
            outputSendMail(email,output)
            return JsonResponse('Child credentials deleted succefully',safe=False)
        except PRIMARY_HEALTH_CENTER.models.Child.DoesNotExist:
            return JsonResponse("invalid registerby id or Child Id", safe=False)
    except PRIMARY_HEALTH_CENTER.models.Admin.DoesNotExist:
            return JsonResponse("invalid admin id or password", safe=False)


def forgot_password(request):
    id=request.POST.get('id')
    try:
        data=Users.objects.get(user_id=id)
        pwd=password_gen()
        data.password=pwd
        data.save()
        outputSendMail(data.email,pwd)
        return JsonResponse('your password have sent to registerd email id',safe=False)
    except PRIMARY_HEALTH_CENTER.models.Users.DoesNotExist:
        try:
            data=Admin.objects.get(admin_id=id)
            pwd=password_gen()
            data.password=pwd
            data.save()
            outputSendMail(data.email,pwd)
            return JsonResponse('your password sent to registerd email id',safe=False)
        except PRIMARY_HEALTH_CENTER.models.Admin.DoesNotExist:
            return JsonResponse("invalid id entered", safe=False)
        
        
def change_password(request):
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


def vaccination_reminder_mail():
    # Get today's date
    today_date = date.today()
    
    match_child_vac_dates = ChildVaccination.objects.filter(Q(vaccination_1month=today_date) |
                                                            Q(vaccination_2month=today_date) |
                                                            Q(vaccination_3month=today_date) |
                                                            Q(vaccination_6month=today_date) |
                                                            Q(vaccination_7month=today_date) |
                                                            Q(vaccination_8month=today_date) |
                                                            Q(vaccination_9month=today_date) |
                                                            Q(vaccination_12month=today_date) |
                                                            Q(vaccination_15month=today_date) |
                                                            Q(vaccination_18month=today_date) |
                                                            Q(vaccination_24month=today_date) |
                                                            Q(vaccination_36month=today_date) |
                                                            Q(vaccination_48month=today_date) |
                                                            Q(vaccination_60month=today_date)
                                                            )
    
    for data in match_child_vac_dates:
        send_mail("VACCINATION REMAINDER",
                  "Your child should be vaccinated within this week. Please kindly visit your near PRIMARY HEALTH CENTER.",
                  "phchol06082001@gmail.com",
                  [data.email])
    
    for data in match_child_vac_dates:
        replace="remaining"
        today=str(today_date)
        if data.vaccination_1month==today:
            data.vaccination_1month=replace
            data.save()
            # print(replace)
        elif data.vaccination_2month==today:
            data.vaccination_2month=replace
            data.save()
        elif data.vaccination_3month==today:
            data.vaccination_3month=replace
            data.save()
        elif data.vaccination_6month==today:
            data.vaccination_6month=replace
            data.save()
        elif data.vaccination_7month==today:
            data.vaccination_7month=replace
            data.save()
        elif data.vaccination_8month==today:
            data.vaccination_8month=replace
            data.save()
        elif data.vaccination_9month==today:
            data.vaccination_9month=replace
            data.save()
        elif data.vaccination_12month==today:
            data.vaccination_12month=replace
            data.save()
        elif data.vaccination_15month==today:
            data.vaccination_15month=replace
            data.save()
        elif data.vaccination_18month==today:
            data.vaccination_18month=replace
            data.save()
        elif data.vaccination_24month==today:
            data.vaccination_24month=replace
            data.save()
        elif data.vaccination_36month==today:
            data.vaccination_36month=replace
            data.save()
        elif data.vaccination_48month==today:
            data.vaccination_48month=replace
            data.save()
        elif data.vaccination_60month==today:
            data.vaccination_60month=replace
            data.save()


vaccination_reminder_mail()


# from django.db.models import F

# def vaccination_reminder_mail():
#     # Get today's date
#     today_date = date.today()

#     # Define the fields and their corresponding replacements
#     fields_to_update = {
#         'vaccination_1month': 'remaining',
#         'vaccination_2month': 'remaining',
#         'vaccination_3month': 'remaining',
#         'vaccination_6month': 'remaining',
#         'vaccination_7month': 'remaining',
#         'vaccination_8month': 'remaining',
#         'vaccination_9month': 'remaining',
#         'vaccination_12month': 'remaining',
#         'vaccination_15month': 'remaining',
#         'vaccination_18month': 'remaining',
#         'vaccination_24month': 'remaining',
#         'vaccination_36month': 'remaining',
#         'vaccination_48month': 'remaining',
#         'vaccination_60month': 'remaining',
#     }

#     # Update matching records in bulk
#     match_child_vac_dates = ChildVaccination.objects.filter(
#         **{f'{field}': today_date for field in fields_to_update.keys()}
#     )
    
#     # Send reminder emails
#     for data in match_child_vac_dates:
#         send_mail("VACCINATION REMINDER",
#                   "Your child should be vaccinated within this week. Please kindly visit your nearest PRIMARY HEALTH CENTER.",
#                   "phchol06082001@gmail.com",
#                   [data.email])

#     # Bulk update vaccination dates
#     for field, replacement in fields_to_update.items():
#         match_child_vac_dates.update(**{field: replacement})

# vaccination_reminder_mail()m