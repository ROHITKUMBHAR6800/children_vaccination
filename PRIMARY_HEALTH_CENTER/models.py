from django.db import models

# Create your models here.
class Admin(models.Model):
    admin_id=models.CharField(max_length=100)
    hospital_name=models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=13)
    email = models.EmailField()
    area_add = models.CharField(max_length=200)
    village_town = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10) 
    tehsil = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def save(self):
        if not self.admin_id:
            # Get the highest existing user_id in the database
            last_admin = Admin.objects.order_by('-admin_id').first()
            if last_admin:
                idDigit=int(last_admin.admin_id[7::])
                #increament last admin id by 1
                makeId="admin00"+str(idDigit+1)
            else:
                # create as 'admin001' 
                makeId="admin00"+str(1)
            self.admin_id = makeId
        super().save()


class Users(models.Model):
    user_id=models.CharField(max_length=100)
    admin_id=models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100) 
    gender=models.CharField(max_length=10)
    mobile_no = models.CharField(max_length=13)
    email = models.EmailField()
    home_add = models.CharField(max_length=200)
    village = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10) 
    tehsil = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def save(self):
        if not self.user_id:
            # Get the highest existing user_id in the database
            last_user = Users.objects.order_by('-user_id').first()
            if last_user:
                idDigit=int(last_user.user_id[6::])
                #increament last admin id by 1
                makeId="user00"+str(idDigit+1)
            else:
                # create as 'user001' 
                makeId="user00"+str(1)
            self.user_id = makeId
        super().save()


class Child(models.Model):
    child_id=models.CharField(primary_key=True,max_length=50)
    register_by=models.CharField(max_length=100)
    child_name=models.CharField(max_length=100)
    father_name=models.CharField(max_length=100)
    surname=models.CharField(max_length=100)
    mother_name=models.CharField(max_length=100)
    birth_date=models.DateField()
    gender=models.CharField(max_length=10)
    mobile_no=models.CharField(max_length=13)
    email=models.EmailField()
    home_add = models.CharField(max_length=200)
    village = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10) 
    tehsil = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

class ChildVaccination(models.Model):
    child = models.ForeignKey(Child,on_delete=models.CASCADE)
    email=models.EmailField()  
    vaccination_1month=models.CharField(max_length=30)
    vaccination_2month=models.CharField(max_length=30)
    vaccination_3month=models.CharField(max_length=30)
    vaccination_6month=models.CharField(max_length=30)
    vaccination_7month=models.CharField(max_length=30)
    vaccination_8month=models.CharField(max_length=30)
    vaccination_9month=models.CharField(max_length=30)
    vaccination_12month=models.CharField(max_length=30)
    vaccination_15month=models.CharField(max_length=30)
    vaccination_18month=models.CharField(max_length=30)
    vaccination_24month=models.CharField(max_length=30)
    vaccination_36month=models.CharField(max_length=30)
    vaccination_48month=models.CharField(max_length=30)
    vaccination_60month=models.CharField(max_length=30)
     
