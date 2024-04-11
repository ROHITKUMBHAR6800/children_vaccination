from datetime import date
from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Q
from CHILD_VACCINATION import settings
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
    
    
    # def add_months_to_date(birth_date_str, months_to_add):
    #         birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
    #         new_date = birth_date + relativedelta(months=months_to_add)
    #         return new_date.strftime('%Y-%m-%d')
    
    # child_ref_var = Child.objects.get(pk=childId)
    # childVaccRefVar=ChildVaccination(
    #                 child=child_ref_var,
    #                 email=mail,
    #                 vaccination_1month = add_months_to_date(birth_date, 1),
    #                 vaccination_2month = add_months_to_date(birth_date, 2),
    #                 vaccination_3month = add_months_to_date(birth_date, 3),
    #                 vaccination_6month = add_months_to_date(birth_date, 6),
    #                 vaccination_7month = add_months_to_date(birth_date, 7),
    #                 vaccination_8month = add_months_to_date(birth_date, 8),
    #                 vaccination_9month = add_months_to_date(birth_date, 9),
    #                 vaccination_12month = add_months_to_date(birth_date, 12),
    #                 vaccination_15month = add_months_to_date(birth_date, 15),
    #                 vaccination_18month = add_months_to_date(birth_date, 18),
    #                 vaccination_24month = add_months_to_date(birth_date, 24),
    #                 vaccination_36month = add_months_to_date(birth_date, 36),
    #                 vaccination_48month = add_months_to_date(birth_date, 48),
    #                 vaccination_60month = add_months_to_date(birth_date, 60)
    #             )
    # childVaccRefVar.save()


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
        
    except Exception as e:
        print(e)


# def vaccination_reminder_mail():
#     # Get today's date
#     today_date = date.today()
    
#     match_child_vac_dates = ChildVaccination.objects.filter(Q(vaccination_1month = today_date) |
#                                                             Q(vaccination_2month = today_date) |
#                                                             Q(vaccination_3month = today_date) |
#                                                             Q(vaccination_6month = today_date) |
#                                                             Q(vaccination_7month = today_date) |
#                                                             Q(vaccination_8month = today_date) |
#                                                             Q(vaccination_9month = today_date) |
#                                                             Q(vaccination_12month = today_date) |
#                                                             Q(vaccination_15month = today_date) |
#                                                             Q(vaccination_18month = today_date) |
#                                                             Q(vaccination_24month = today_date) |
#                                                             Q(vaccination_36month = today_date) |
#                                                             Q(vaccination_48month = today_date) |
#                                                             Q(vaccination_60month = today_date)
#                                                             )
    
#     mail_list = []
#     for data in match_child_vac_dates:
#         mail_list.append(data.email)

#     send_mail("VACCINATION REMAINDER",
#             "Your child should be vaccinated within this week. Please kindly visit your near PRIMARY HEALTH CENTER.",
#             "phchol06082001@gmail.com",
#             mail_list)
    
#     replace="remaining"
#     child_list = []
#     for data in match_child_vac_dates:
#         today=str(today_date)
#         if data.vaccination_1month == today:
#             data.vaccination_1month =replace

#         elif data.vaccination_2month == today:
#             data.vaccination_2month =replace
           
#         elif data.vaccination_3month == today:
#             data.vaccination_3month =replace
           
#         elif data.vaccination_6month == today:
#             data.vaccination_6month =replace
           
#         elif data.vaccination_7month == today:
#             data.vaccination_7month =replace
            
#         elif data.vaccination_8month == today:
#             data.vaccination_8month =replace
           
#         elif data.vaccination_9month == today:
#             data.vaccination_9month =replace
            
#         elif data.vaccination_12month == today:
#             data.vaccination_12month =replace
            
#         elif data.vaccination_15month == today:
#             data.vaccination_15month =replace
            
#         elif data.vaccination_18month == today:
#             data.vaccination_18month =replace
            
#         elif data.vaccination_24month == today:
#             data.vaccination_24month =replace
          
#         elif data.vaccination_36month == today:
#             data.vaccination_36month =replace
            
#         elif data.vaccination_48month == today:
#             data.vaccination_48month =replace
           
#         elif data.vaccination_60month == today:
#             data.vaccination_60month =replace
        
#         data.save()

#     # child_list.save()

# # vaccination_reminder_mail()
