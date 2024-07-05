from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Q
from PRIMARY_HEALTH_CENTER.models import ChildVaccination,Child
from CHILD_VACCINATION import settings
from datetime import datetime,date
from dateutil.relativedelta import relativedelta


@shared_task(bind= True)
def send_updates(self,reciever,sub,mes):
    subject = sub
    message = f"This is system generated mail from child vaccination portal.{mes}"
    sender = settings.EMAIL_HOST_USER

    send_mail(subject, message, sender, [reciever],fail_silently=True)


@shared_task(bind= True)
def insertIntoChildVaccModel(self,childId,mail,birth_date_str):

    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')

    months_list=(1,2,3,6,7,8,9,12,15,18,24,36,48,60)
    vaccinations = {}
    for i in months_list:
        vaccinations[f'vaccination_{i}month'] = (birth_date + relativedelta(months=i)).strftime('%Y-%m-%d')

    child_ref_var = Child.objects.get(pk=childId)
    childVaccRefVar = ChildVaccination(child=child_ref_var, email=mail, **vaccinations)
    childVaccRefVar.save()

    
@shared_task(bind= True)
def vaccination_notification(self):
    try:
        # Get today's date
        today_date = date.today()
        
        matchedData = ChildVaccination.objects.filter(
                        Q(vaccination_1month = today_date) | Q(vaccination_2month = today_date) |
                        Q(vaccination_3month = today_date) | Q(vaccination_6month = today_date) |
                        Q(vaccination_7month = today_date) | Q(vaccination_8month = today_date) |
                        Q(vaccination_9month = today_date) | Q(vaccination_12month = today_date) |
                        Q(vaccination_15month = today_date) | Q(vaccination_18month = today_date) |
                        Q(vaccination_24month = today_date) | Q(vaccination_36month = today_date) |
                        Q(vaccination_48month = today_date) | Q(vaccination_60month = today_date)
                        )
        
        if len(matchedData)>0:
            email_list = []
            for data in matchedData:
                email_list.append(data.email)

            subject = "VACCINATION REMAINDER"
            message = "Your child should be vaccinated within this week. Please kindly visit your near PRIMARY HEALTH CENTER."
            sender = settings.EMAIL_HOST_USER

            send_mail(subject, message, sender, email_list)
        
            # replace="remaining"
            # # child_list = []
            # for data in matchedData:
            #     today=str(today_date)
            #     if data.vaccination_1month == today:
            #         data.vaccination_1month = replace
            #     elif data.vaccination_2month == today:
            #         data.vaccination_2month = replace
            #     elif data.vaccination_3month == today:
            #         data.vaccination_3month = replace
            #     elif data.vaccination_6month == today:
            #         data.vaccination_6month = replace
            #     elif data.vaccination_7month == today:
            #         data.vaccination_7month = replace   
            #     elif data.vaccination_8month == today:
            #         data.vaccination_8month = replace
            #     elif data.vaccination_9month == today:
            #         data.vaccination_9month = replace     
            #     elif data.vaccination_12month == today:
            #         data.vaccination_12month = replace      
            #     elif data.vaccination_15month == today:
            #         data.vaccination_15month = replace        
            #     elif data.vaccination_18month == today:
            #         data.vaccination_18month = replace        
            #     elif data.vaccination_24month == today:
            #         data.vaccination_24month = replace   
            #     elif data.vaccination_36month == today:
            #         data.vaccination_36month = replace     
            #     elif data.vaccination_48month == today:
            #         data.vaccination_48month = replace 
            #     elif data.vaccination_60month == today:
            #         data.vaccination_60month = replace
            #     data.save() 
            
            replace = "remaining"
            for data in matchedData:
                today = str(today_date)
                fields_to_update = [
                    'vaccination_1month', 'vaccination_2month', 'vaccination_3month',
                    'vaccination_6month', 'vaccination_7month', 'vaccination_8month',
                    'vaccination_9month', 'vaccination_12month', 'vaccination_15month',
                    'vaccination_18month', 'vaccination_24month', 'vaccination_36month',
                    'vaccination_48month', 'vaccination_60month'
                ]
                for field in fields_to_update:
                    if getattr(data, field) == today:
                        setattr(data, field, replace)
                data.save()
   
    except Exception as e:
        print(e)

