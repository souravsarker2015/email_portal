from django.http import HttpResponse
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'email_app/home/home.html'


def success_message(request):
    return HttpResponse("successful")
