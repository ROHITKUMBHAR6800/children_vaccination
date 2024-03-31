from datetime import datetime
import celery
from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Q

from CHILD_VACCINATION.celery import app
from .models import ChildVaccination
from django.conf import settings


@shared_task(bind=True)
def op_send_email(self):
    print('hi here')
    return "Done"


@app.task(name='op_send_email_notification')
def op_send_email_notification():
    try:
        # Get today's date
        today_date = datetime.today()
        
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
        
        SUBJECT = "VACCINATION REMAINDER"
        MESSAGE = "Your child should be vaccinated within this week. Please kindly visit your near PRIMARY HEALTH CENTER."
        EMAIL_FROM = settings.EMAIL_HOST_USER
        email_id_list = []
        for data in match_child_vac_dates:
            email_id_list.append(data.email)
        
        print(['rohitkumbhar638@gmail.com'])

        send_mail(SUBJECT, MESSAGE, EMAIL_FROM, ['rohitkumbhar638@gmail.com'])
        
    except Exception as e:
        print(e)