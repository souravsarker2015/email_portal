from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView

from email_app.forms import ScheduleForm
from email_app.models import Schedule, Recipient, Email, ScheduleContent
from dateutil import parser

import ast


class ScheduleViews(View):
    def get(self, request):
        recipients = Recipient.objects.all().order_by("-created")
        emails = Email.objects.all().order_by("-created")
        data = {
            'recipients': recipients,
            'emails': emails
        }
        return render(request, 'email_app/schedule/add_schedule1.html', data)

    def post(self, request):
        recipients = request.POST.getlist('recipients')
        subject = request.POST.get('subject')
        datetime = request.POST.get('schedule_time')
        input_date = parser.parse(datetime)
        print(f"{recipients} \n {subject} \n {input_date}")
        ScheduleContent.objects.create(email=recipients, subject=subject, schedule=input_date)

        return redirect("schedule-created")


# class ScheduleViews(View):
#     def get(self, request):
#         form = ScheduleForm()
#         return render(request, 'email_app/schedule/add_schedule1.html', {'form': form})
#
#     def post(self, request):
#         form = ScheduleForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect("schedule-list")


class ScheduleListView(ListView):
    model = ScheduleContent
    template_name = 'email_app/schedule/schedule_list.html'
    context_object_name = 'schedules'
    ordering = ["-created"]


class ScheduleDetailView(DetailView):
    model = ScheduleContent
    context_object_name = 'schedule'
    template_name = 'email_app/schedule/schedule_details.html'


class ScheduleUpdateView(View):
    def get(self, request, pk):
        schedule = ScheduleContent.objects.get(pk=pk)
        recipients = Recipient.objects.all().order_by("-created")
        emails = Email.objects.all().order_by("-created")
        sc = ScheduleContent.objects.get(pk=pk)
        s = sc.email
        print(s)
        ss = ast.literal_eval(s)

        data = {
            'schedule': schedule,
            'recipients': recipients,
            'emails': emails,
            'ss': ss,
        }
        return render(request, "email_app/schedule/schedule_update1.html", data)

    def post(self, request, pk):
        schedule = ScheduleContent.objects.get(pk=pk)
        email = request.POST.getlist('recipients')
        subject = request.POST.get('subject')
        schedule_time = request.POST.get('schedule_time')
        schedule.email = email
        schedule.subject = subject
        schedule.schedule = schedule_time
        schedule.save()
        return redirect('schedule-list')
    # model = Schedule
    # form_class = ScheduleForm
    # template_name = 'email_app/schedule/schedule_update.html'
    # success_url = '/admin/schedules/'


class ScheduleDeleteView(DeleteView):
    model = ScheduleContent
    template_name = 'email_app/schedule/schedule_delete.html'
    success_url = '/admin/schedules/'


class ScheduleCreated(TemplateView):
    template_name = 'email_app/schedule/schedule_created.html'
