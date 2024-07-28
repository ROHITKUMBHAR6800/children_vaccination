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
    vaccinations_dates = {}
    for i in months_list:
        vaccinations_dates[f'vaccination_{i}month'] = (birth_date + relativedelta(months=i)).strftime('%Y-%m-%d')
    child_primary_key = Child.objects.get(pk=childId)
    childVaccRefVar = ChildVaccination(child=child_primary_key, email=mail, **vaccinations_dates)
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
        
            replace = "remaining"
            today = str(today_date)
            fields_to_update = [
                    'vaccination_1month', 'vaccination_2month', 'vaccination_3month',
                    'vaccination_6month', 'vaccination_7month', 'vaccination_8month',
                    'vaccination_9month', 'vaccination_12month', 'vaccination_15month',
                    'vaccination_18month', 'vaccination_24month', 'vaccination_36month',
                    'vaccination_48month', 'vaccination_60month'
                ]
            for data in matchedData:
                updated=False
                for field in fields_to_update:
                    if getattr(data, field) == today:
                        setattr(data, field, replace)
                        updated=True
                if updated:
                    data.save()
   
    except Exception as e:
        print(e)

