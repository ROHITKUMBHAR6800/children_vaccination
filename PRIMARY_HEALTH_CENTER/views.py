from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from random import randint
from django.core.mail import send_mail
import PRIMARY_HEALTH_CENTER
from PRIMARY_HEALTH_CENTER.models import *
from django.db.models import Q
from smtplib import SMTPException, SMTPRecipientsRefused
from CHILD_VACCINATION import settings
from PRIMARY_HEALTH_CENTER.tasks import insertIntoChildVaccModel,send_updates
from datetime import datetime
from dateutil.relativedelta import relativedelta

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

def userRegistrationForm(request):
    return render(request, "userRegistretionForm.html")

def childRegistrationForm(request):
    return render(request, "childRegistrationForm.html")


def admin_registration(request):
    if request.method == 'POST':
        mail=request.POST.get("email")
        if len(Admin.objects.filter(email=mail))>0:
            return JsonResponse("email id or user exist already",safe=False)

        password=request.POST.get("password")
        confirm_password=request.POST.get("confirmPassword")
        if password!=confirm_password:
            return JsonResponse("both password are different",safe=False)
        
        ot = otp()
        output = send_otp(mail,ot)
        if output == False:
            return JsonResponse("invalid email id",safe = False)
        
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
        
        ot = otp()
        output = send_otp(mail,ot)
        if output == False:
            return JsonResponse("invalid email id",safe = False)
        
        usersRefVar=Users(admin_id=adminId,
                        user_name=request.POST.get("userName"),
                        middle_name=request.POST.get("middleName"),
                        surname=request.POST.get("surname"),
                        gender=request.POST.get("gender"),
                        mobile_no=request.POST.get("mobile"),
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
        childId="ch00-"+str(bcid)
        if len(Child.objects.filter(child_id=childId))>0:
            return JsonResponse("child registered already",safe=False)
        
        birth_date=request.POST.get("birthDate") 
        mail=request.POST.get("email")
        
        registerBy=request.POST.get("registerBy")
        pwd=request.POST.get("password")
        try:
            Users.objects.get(user_id=registerBy,password=pwd)
        except PRIMARY_HEALTH_CENTER.models.Users.DoesNotExist:
            try:
                Admin.objects.get(admin_id=registerBy,password=pwd)
            except PRIMARY_HEALTH_CENTER.models.Admin.DoesNotExist:
                return JsonResponse("invalid id or password", safe=False)
            
        ot = otp()
        output = send_otp(mail,ot)
        if output == False:
            return JsonResponse("invalid email id",safe = False)

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
                return JsonResponse("Child registration is successfull",safe=False)
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
        childId=request.POST.get("childId")
        try:
            data=Child.objects.get(child_id=childId)
            mail=data.email
            data.delete()
            sub="CREDINTAILS DELETED BY ADMIN"
            mes ="Your credintials deleted by admin, you are not longer participant."
            send_updates(mail,sub,mes)
            return JsonResponse('Child credentials deleted succefully',safe=False)
        except PRIMARY_HEALTH_CENTER.models.Child.DoesNotExist:
            return JsonResponse("invalid registerby id or Child Id", safe=False)
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


# def admin_page(request):
#     if request.method != "POST":
#         return JsonResponse("invalid method",safe=False)
#     adminId = request.POST.get("adminId")
#     pwd = request.POST.get("password")
#     try:
#         admin_data=Admin.objects.get(admin_id=adminId,password=pwd)
#         hospital_name=admin_data.hospital_name
#         hospital_add=f"{admin_data.area_add}, {admin_data.village_town}, Tehsil-{admin_data.tehsil}, District-{admin_data.district}, State-{admin_data.state}, India."
#         users_object=Users.objects.filter(admin_id=admin_data.admin_id)
#         user_data={}
#         for user in users_object:
#             user_data[user.user_id]=userData(user)
#         users_count=len(users_object)
#         all_children_object=[]
#         user_children_object={}
#         if users_count>0:
#             if len(Child.objects.filter(register_by=adminId))>0:
#                 user_children_object[admin_data] =(Child.objects.filter(register_by=admin_data.admin_id))
#             for user in users_object:
#                 all_children_object.extend(Child.objects.filter(register_by=user.user_id))
#                 user_children_object[user] =(Child.objects.filter(register_by=user.user_id))
#             if len(Child.objects.filter(register_by=adminId))>0:
#                 all_children_object.extend(Child.objects.filter(register_by=admin_data.admin_id))
#         children_count=len(all_children_object)
#         admin_data={"admin_id":adminId,"hospital_name":hospital_name,"hospital_add":hospital_add,"userCount":users_count,"usersInfo":user_data,"childCount":children_count, "childrenInfo":all_children_object}
#         return render(request,"adminPage.html",admin_data)
#     except PRIMARY_HEALTH_CENTER.models.Admin.DoesNotExist:
#         return JsonResponse("invalid credintials",safe=False)
    

def admin_page(request):
    if request.method != "POST":
        return JsonResponse("invalid method", safe=False)
    
    adminId = request.POST.get("adminId")
    pwd = request.POST.get("password")
    
    try:
        admin_data = Admin.objects.get(admin_id=adminId, password=pwd)
        hospital_name = admin_data.hospital_name
        hospital_add = f"{admin_data.area_add}, {admin_data.village_town}, Tehsil-{admin_data.tehsil}, District-{admin_data.district}, State-{admin_data.state}, India."
        users_object = Users.objects.filter(admin_id=admin_data.admin_id)
        user_data = {user.user_id: userData(user) for user in users_object}
        users_count = len(users_object)
        
        all_children_object = []
        if users_count > 0:
            if Child.objects.filter(register_by=adminId).exists():
                all_children_object.extend(Child.objects.filter(register_by=adminId))
            for user in users_object:
                all_children_object.extend(Child.objects.filter(register_by=user.user_id))
        
        children_count = len(all_children_object)
        admin_data = {
            "admin_id": adminId,
            "hospital_name": hospital_name,
            "hospital_add": hospital_add,
            "userCount": users_count,
            "usersInfo": user_data,
            "childCount": children_count,
            "childrenInfo": all_children_object
        }
        return render(request, "adminPage.html", admin_data)
    except Admin.DoesNotExist:
        return JsonResponse("invalid credentials", safe=False)

def user_page(request):
    if request.method != "POST":
        return JsonResponse("invalid method", safe=False)
    userId = request.POST.get("userId")
    pwd = request.POST.get("password")
    try:
        user_data=Users.objects.get(user_id=userId, password=pwd)
        data=userData(user_data)
        return render(request,"userPage.html",data)
    except PRIMARY_HEALTH_CENTER.models.Users.DoesNotExist:
        return JsonResponse("invalid credintials",safe=False)
    
# def userData(user_data):
#         admin_data=Admin.objects.get(admin_id=user_data.admin_id)
#         user_name=f"{user_data.user_name} {user_data.middle_name} {user_data.surname}."
#         hospital_name=admin_data.hospital_name
#         hospital_add=f"{admin_data.area_add}, {admin_data.village_town}, Tehsil-{admin_data.tehsil}, District-{admin_data.district}, State-{admin_data.state}, India."
#         children_object=Child.objects.filter(register_by=user_data.user_id)
#         children_count=len(children_object)

#         def queryset_to_dict_list(queryset):
#             return [obj.child_id for obj in queryset]
        
#         # Filter the Child records based on ChildVaccination records where vaccination_1month contains matching data
#         months_wise_remain=give_vacc_remain_data(children_object)

#         totalRemainCount=0
#         totalRemainData={}
#         for key,value in months_wise_remain.items():
#             totalRemainData[key]=queryset_to_dict_list(value)
#             totalRemainCount+=len(value)
        
#         # Get today's date
#         endDate = datetime.today()
#         # Calculate start date by subtracting one month from today's date
#         startDate = endDate - relativedelta(months=1)
#         # This will always show vaccination done data within one month
#         months_wise_done=give_vacc_done_data(children_object,startDate,endDate)

#         totalDoneCount=0
#         totalDoneData={}
#         for key,value in months_wise_done.items():
#             totalDoneData[key]=queryset_to_dict_list(value)
#             totalDoneCount=len(value)
#         data={"user_name":user_name,"hospital_name":hospital_name,"hospital_add":hospital_add,"childCount":children_count,"totalDone":totalDoneCount,"totalRemain":totalRemainCount,"doneData":totalDoneData,"remainData":totalRemainData}
#         return data
    

def userData(user_data):
    admin_data = Admin.objects.get(admin_id=user_data.admin_id)
    user_name = f"{user_data.user_name} {user_data.middle_name} {user_data.surname}."
    hospital_name = admin_data.hospital_name
    hospital_add = f"{admin_data.area_add}, {admin_data.village_town}, Tehsil-{admin_data.tehsil}, District-{admin_data.district}, State-{admin_data.state}, India."
    children_object = Child.objects.filter(register_by=user_data.user_id)
    children_count = len(children_object)

    def queryset_to_dict_list(queryset):
        return [obj.child_id for obj in queryset]

    months_wise_remain = give_vacc_remain_data(children_object)
    totalRemainCount = sum(len(v) for v in months_wise_remain.values())
    totalRemainData = {k: queryset_to_dict_list(v) for k, v in months_wise_remain.items()}

    endDate = datetime.today()
    startDate = endDate - relativedelta(months=1)
    months_wise_done = give_vacc_done_data(children_object, startDate, endDate)
    totalDoneCount = sum(len(v) for v in months_wise_done.values())
    totalDoneData = {k: queryset_to_dict_list(v) for k, v in months_wise_done.items()}

    return {
        "user_name": user_name,
        "hospital_name": hospital_name,
        "hospital_add": hospital_add,
        "childCount": children_count,
        "totalDone": totalDoneCount,
        "totalRemain": totalRemainCount,
        "doneData": totalDoneData,
        "remainData": totalRemainData
    }



def user_detail(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    user_info = userData(user)
    return render(request, 'user_detail.html', user_info)

def child_detail(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    return render(request, 'child_detail.html', {'child': child})

def give_vacc_remain_data(children_object):
    # Filter the Child records based on ChildVaccination records where vaccination_1month contains matching data
    months_wise_remain={}
    months_wise_remain['month1_vacc_remain'] = children_object.filter(childvaccination__vaccination_1month = 'remaining')
    months_wise_remain['month2_vacc_remain'] = children_object.filter(childvaccination__vaccination_2month = 'remaining')
    months_wise_remain['month3_vacc_remain'] = children_object.filter(childvaccination__vaccination_3month = 'remaining')
    months_wise_remain['month6_vacc_remain'] = children_object.filter(childvaccination__vaccination_6month = 'remaining')
    months_wise_remain['month7_vacc_remain'] = children_object.filter(childvaccination__vaccination_7month = 'remaining')
    months_wise_remain['month8_vacc_remain'] = children_object.filter(childvaccination__vaccination_8month = 'remaining')
    months_wise_remain['month9_vacc_remain'] = children_object.filter(childvaccination__vaccination_9month = 'remaining')
    months_wise_remain['month12_vacc_remain'] = children_object.filter(childvaccination__vaccination_12month = 'remaining')
    months_wise_remain['month15_vacc_remain'] = children_object.filter(childvaccination__vaccination_15month = 'remaining')
    months_wise_remain['month18_vacc_remain'] = children_object.filter(childvaccination__vaccination_18month = 'remaining')
    months_wise_remain['month24_vacc_remain'] = children_object.filter(childvaccination__vaccination_24month = 'remaining')
    months_wise_remain['month36_vacc_remain'] = children_object.filter(childvaccination__vaccination_36month = 'remaining')
    months_wise_remain['month48_vacc_remain'] = children_object.filter(childvaccination__vaccination_48month = 'remaining')
    months_wise_remain['month60_vacc_remain'] = children_object.filter(childvaccination__vaccination_60month = 'remaining')
    return months_wise_remain
    

def give_vacc_done_data(children_object,startDate,endDate):
    months_wise_done={}
    months_wise_done['month1_vacc_done'] = children_object.filter(childvaccination__vaccination_1month__range=(startDate, endDate))
    months_wise_done['month2_vacc_done'] = children_object.filter(childvaccination__vaccination_2month__range=(startDate, endDate))
    months_wise_done['month3_vacc_done'] = children_object.filter(childvaccination__vaccination_3month__range=(startDate, endDate))
    months_wise_done['month6_vacc_done'] = children_object.filter(childvaccination__vaccination_6month__range=(startDate, endDate))
    months_wise_done['month7_vacc_done'] = children_object.filter(childvaccination__vaccination_7month__range=(startDate, endDate))
    months_wise_done['month8_vacc_done'] = children_object.filter(childvaccination__vaccination_8month__range=(startDate, endDate))
    months_wise_done['month9_vacc_done'] = children_object.filter(childvaccination__vaccination_9month__range=(startDate, endDate))
    months_wise_done['month12_vacc_done'] = children_object.filter(childvaccination__vaccination_12month__range=(startDate, endDate))
    months_wise_done['month15_vacc_done'] = children_object.filter(childvaccination__vaccination_15month__range=(startDate, endDate))
    months_wise_done['month18_vacc_done'] = children_object.filter(childvaccination__vaccination_18month__range=(startDate, endDate))
    months_wise_done['month24_vacc_done'] = children_object.filter(childvaccination__vaccination_24month__range=(startDate, endDate))
    months_wise_done['month36_vacc_done'] = children_object.filter(childvaccination__vaccination_36month__range=(startDate, endDate))
    months_wise_done['month48_vacc_done'] = children_object.filter(childvaccination__vaccination_48month__range=(startDate, endDate))
    months_wise_done['month60_vacc_done'] = children_object.filter(childvaccination__vaccination_60month__range=(startDate, endDate))
    return months_wise_done
    
    

def vacc_remaind_again(request):
    if request.method != "POST":
        return JsonResponse("Invalid method", safe=False)
    
    childId = request.POST.get('childId')
    if not childId:
        return JsonResponse("Child ID is required", safe=False)
    
    try:
        data = Child.objects.get(child_id=childId)
        sub = "VACCINATE CHILD ON TIME"
        mes = "Your child vaccination is still remaining. Please visit your nearest PRIMARY HEALTH CENTER for vaccination within two days."
        send_updates(data.email, sub, mes)
        return JsonResponse("Reminder sent successfully", safe=False)
    except Child.DoesNotExist:
        return JsonResponse("Invalid child ID", safe=False)

    
    
def vacc_done(request):
    if request.method != "POST":
        return JsonResponse("Invalid method", safe=False)
    childId = request.POST.get('childId')
    try:
        data = ChildVaccination.objects.get(child_id=childId)
        remaining_vaccination_fields = ['vaccination_1month','vaccination_2month', 'vaccination_3month','vaccination_6month', 'vaccination_7month', 
                                        'vaccination_8month', 'vaccination_9month', 'vaccination_12month','vaccination_15month', 'vaccination_18month', 
                                        'vaccination_24month', 'vaccination_36month', 'vaccination_48month', 'vaccination_60month'
                                        ]
        current_time = datetime.now()
        for field in remaining_vaccination_fields:
            if getattr(data, field) == "remaining":
                setattr(data, field, current_time)
        data.save()
        return JsonResponse("Vaccination done", safe=False)
        
    except ChildVaccination.DoesNotExist:
        return JsonResponse("Invalid registerby id or Child Id", safe=False)


def search_vacc_done(request):
    id=request.POST.get("id")
    startDate=request.POST.get("startDate")
    endDate=request.POST.get("endDate")
    try:
        children_object=Child.objects.filter(register_by=id)

        # Convert the endDate string to a datetime object
        endDate_strp = datetime.strptime(endDate, '%Y-%m-%d')

        # Add one day to endDate using relativedelta and convert it to a string
        newEndDate = (endDate_strp + relativedelta(days=1)).strftime('%Y-%m-%d')
        months_wise_done=give_vacc_done_data(children_object,startDate,newEndDate)

        sum1=0
        for item in months_wise_done:
            data=months_wise_done[item]
            sum1+=len(data)
        return JsonResponse(f"{sum1}",safe=False)
    except PRIMARY_HEALTH_CENTER.models.Users.DoesNotExist:
        return JsonResponse("invalid registerby id or Child Id", safe=False)