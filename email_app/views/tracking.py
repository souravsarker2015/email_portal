import os

from django.http import HttpResponse
from django.utils.timezone import now
from django.views.generic import ListView, DetailView, DeleteView

from email_app.models import Email, Recipient, TrackedRecipients


def email_seen(request, r_id, e_id):
    r = Recipient.objects.get(id=r_id)
    e = Email.objects.get(id=e_id)
    TrackedRecipients.objects.create(recipient=r.email_address, subject=e.subject, seen_time=now())
    print("Successfully Tracked")

    with open(os.path.dirname(os.path.abspath(__file__)) + "/res/1x1.png", "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")


def email_seen_(request, r_email, e_id):
    e = Email.objects.get(id=e_id)
    TrackedRecipients.objects.create(recipient=r_email, subject=e.subject, seen_time=now())
    print("Successfully Tracked")

    with open(os.path.dirname(os.path.abspath(__file__)) + "/res/1x1.png", "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")


class TrackedRecipientListView(ListView):
    model = TrackedRecipients
    template_name = 'email_app/tracking/tracked_recipient.html'
    context_object_name = 'recipients'
    ordering = ["-created"]


class TrackedRecipientDetailView(DetailView):
    model = TrackedRecipients
    context_object_name = 'recipient'
    template_name = 'email_app/tracking/tracked_recipient_details.html'


class TrackedRecipientDeleteView(DeleteView):
    model = TrackedRecipients
    template_name = 'email_app/tracking/tracked_recipient_delete.html'
    success_url = '/admin/tracked/recipients/'
