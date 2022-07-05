import logging
import datetime
# from datetime import datetime
import json
# from datetime import datetime as d
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from dateutil import parser

from email_app import config
from email_app.forms import ScheduleForm
from email_app.models import Recipient, Email, Schedule, ScheduleContent
import ast

logger = logging.getLogger(__name__)


# x = dt.strftime("%Y-%m-%d %H:%M:%S")

def mail_schedule_view(request):
    recipients = Recipient.objects.all().order_by("-created")
    emails = Email.objects.all().order_by("-created")
    schedules = Schedule.objects.all().order_by("-created")
    email_addresses = []
    if request.method == "POST":
        email_address = request.POST.getlist("recipients")
        subject = request.POST.get("subject")
        schedule = request.POST.get("schedule")
        s = schedule.replace("p.m.", "PM")
        # mail_schedule(email_address, sub, s)
        ScheduleContent.objects.create(email=email_address, subject=subject, schedule=s)
        return redirect('email-send-success')

    data = {
        'recipients': recipients,
        'emails': emails,
        'schedules': schedules,
    }
    return render(request, "email_app/schedule/email_send_schedule.html", data)


# 2022-07-01 07:40:30
# ['4', 'June 30, 2022, 3:47 p.m.']

# def mail_schedule(email_address, sub, sd):
def mail_schedule():
    data = ScheduleContent.objects.all().last()
    schedule = data.schedule
    em = data.email
    email_addresses = ast.literal_eval(em)
    subject = data.subject
    input_date = parser.parse(schedule)
    time_now = datetime.datetime.now()
    date1 = input_date.strftime("%Y-%m-%d %H:%M")
    date2 = time_now.strftime("%Y-%m-%d %H:%M")
    email = Email.objects.get(subject=subject)
    e_body = email.email_body
    print(f"input_date :{date1} now{date2} email={email} email_b={email.email_body}")
    if date2 == date1:
        recipient_email = []
        for i in email_addresses:
            recipient_email.append(i)
            recipient = Recipient.objects.get(email_address=i)
            email_body = e_body.replace("{name}", recipient.name).replace("{email}", i)
            send_mail(subject, email_body, from_email='souravsarker2015@gmail.com', recipient_list=recipient_email, html_message=email_body)
            recipient_email = []
            logger.info("cron job was called")
    return redirect('email-send-success')

# def mail_schedule():
#     e_d = email_address
#     subject = sub
#     schedule = sd
#     input_date = parser.parse(schedule)
#     time_now = datetime.datetime.now()
#     date1 = input_date.strftime("%Y-%m-%d %H:%M")
#     date2 = time_now.strftime("%Y-%m-%d %H:%M")
#     email = Email.objects.get(subject=subject)
#     body = "test"
#     if date2 == date1:
#         send_mail(subject, email.email_body, from_email='souravsarker2015@gmail.com', recipient_list=e_d)
#         logger.info("cron job was called")
#     return HttpResponse("check")
# def mail_schedule(email_address, sub, sd):
# def mail_schedule():
#     # input_date = parser.parse(sd)
#     time_now = datetime.datetime.now()
#     # date1 = input_date.strftime("%Y-%m-%d %H:%M")
#     date2 = time_now.strftime("%Y-%m-%d %H:%M")
#     date1 = datetime.datetime(2022, 7, 1, 16, 22)
#     date3 = date1.strftime("%Y-%m-%d %H:%M")
#     # print(date1)
#     print(date2)
#     subject = "test"
#     # email = Email.objects.get(subject=subject)
#     body = "test"
#     if date2 == date3:
#         send_mail(subject, body, from_email='souravsarker2015@gmail.com', recipient_list=["sourovsarker007@gmail.com"])
#         logger.info("cron job was called")
#     return HttpResponse("check")
# return render(request, 'email_app/schedule/add_schedule.html')


# d = datetime.strptime(sd, '%B %d, %Y, %I:%M %p')
#     dt = d.strftime("%Y-%m-%d %I:%M")
#     print(dt)
# date1 = datetime.datetime(2022, 6, 30, 20, 2)
# date1 = datetime.datetime(sd)
# print(date1)
# y = d.d.strftime(sd, "%Y-%m-%d %H:%M")
# print(y)
