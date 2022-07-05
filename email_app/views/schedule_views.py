from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from email_app.forms import ScheduleForm
from email_app.models import Schedule


class ScheduleViews(View):
    def get(self, request):
        form = ScheduleForm()
        return render(request, 'email_app/schedule/add_schedule.html', {'form': form})

    def post(self, request):
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("schedule-list")


class ScheduleListView(ListView):
    model = Schedule
    template_name = 'email_app/schedule/schedule_list.html'
    context_object_name = 'schedules'
    ordering = ["-created"]


class ScheduleDetailView(DetailView):
    model = Schedule
    context_object_name = 'schedule'
    template_name = 'email_app/schedule/schedule_details.html'


class ScheduleUpdateView(UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'email_app/schedule/schedule_update.html'
    success_url = '/schedule_list/'


class ScheduleDeleteView(DeleteView):
    model = Schedule
    template_name = 'email_app/schedule/schedule_delete.html'
    success_url = '/schedule_list/'
