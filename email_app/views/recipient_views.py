from datetime import date

from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views import View
from django.views.generic import FormView, ListView, UpdateView, DetailView, DeleteView, TemplateView

from core.models import Country, City, State
from email_app.forms import RecipientForm
from email_app.models import Recipient, Filter


class RecipientFormView(FormView):
    form_class = RecipientForm
    template_name = 'email_app/recipient/add_recipient.html'
    success_url = reverse_lazy('/success/')

    def form_valid(self, form):
        form.save()
        return redirect('recipient-list')


class RecipientListView(ListView):
    model = Recipient
    template_name = 'email_app/recipient/recipient_list.html'
    context_object_name = 'recipients'
    ordering = ["-created"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filters = Filter.objects.all().order_by("-created")
        context['filters'] = filters
        return context


class RecipientDetailView(DetailView):
    model = Recipient
    context_object_name = 'recipient'
    template_name = 'email_app/recipient/recipient_details.html'


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    # fields = '__all__'
    template_name = 'email_app/recipient/recipient_update.html'
    success_url = '/recipient_list/'


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'email_app/recipient/recipient_confirm_delete.html'
    success_url = '/recipient_list/'


def age_to_dob_calculate(arg):
    current = now().date()
    return date(current.year - int(arg), current.month, current.day)


def age_to_dob_calculate_minus(arg):
    current = now().date()
    return date(current.year - int(arg) - 1, current.month, current.day)


def age_to_dob_calculate_plus(arg):
    current = now().date()
    return date(current.year - int(arg) + 1, current.month, current.day)


class RecipientFilter(View):
    def get(self, request):
        return render(request, 'email_app/recipient/recipient_list.html')

    def post(self, request):
        f_id = int(request.POST.get('filters'))
        filter_ = Filter.objects.get(pk=f_id)
        content = filter_.content
        filter_list = content
        print(type(filter_list))
        q = Q()
        if filter_list:
            for value in filter_list:
                col = value['col']
                val = value['value']  # country city state array
                if isinstance(value, dict):
                    if value['value'] != "":
                        if value['op'] == "" or value['op'] == 'and':
                            if col == 'age':
                                if value['eql'] == 'is':
                                    # age = age_to_dob_calculate(value['value'])
                                    age1 = age_to_dob_calculate_minus(value['value'])
                                    age2 = age_to_dob_calculate_plus(value['value'])
                                    q &= q & Q(dob__range=(age1, age2))

                                elif value['eql'] == 'is_more_than':
                                    age = age_to_dob_calculate(value['value'])
                                    q &= q & Q(dob__lt=age)

                                elif value['eql'] == 'is_less_than':
                                    age = age_to_dob_calculate(value['value'])
                                    q &= q & Q(dob__gt=age)

                            if col == 'country':
                                countries = Country.objects.filter(name__in=value['value'])
                                if value['eql'] == 'is':
                                    # for i in value['value']:
                                    q &= q & Q(country_id__in=countries)
                                elif value['eql'] == 'is_not':
                                    q &= q & ~Q(country_id__in=countries)

                            if col == 'state':
                                states = State.objects.filter(name__in=value['value'])
                                if value['eql'] == 'is':
                                    q &= q & Q(state_id__in=states)
                                elif value['eql'] == 'is_not':
                                    q &= q & ~Q(state_id__in=states)

                            if col == 'city':
                                cities = City.objects.filter(name__in=value['value'])
                                if value['eql'] == 'is':
                                    q &= q & Q(city_id__in=cities)
                                elif value['eql'] == 'is not':
                                    q &= q & ~Q(city_id__in=cities)

                            if col == 'email':
                                if value['eql'] == 'are':
                                    q &= q & Q(email_address__in=value['value'])

                                elif value['eql'] == 'are_not':
                                    q &= q & ~Q(email_address__in=value['value'])

                        elif value['op'] == 'or':
                            print("filter list getting")
                            print(value)
                            if col == 'age':
                                if value['eql'] == 'is':
                                    age = age_to_dob_calculate(value['value'])
                                    q |= Q(dob=age)

                                elif value['eql'] == 'is_more_than':
                                    age = age_to_dob_calculate(value['value'])
                                    q |= Q(dob__lt=age)

                                elif value['eql'] == 'is_less_than':
                                    age = age_to_dob_calculate(value['value'])
                                    q |= Q(dob__gt=age)

                            if col == 'country':
                                countries = Country.objects.filter(name__in=value['value'])
                                if value['eql'] == 'is':
                                    q |= Q(country_id__in=countries)
                                elif value['eql'] == 'is_not':
                                    q |= ~Q(country_id__in=countries)

                            if col == 'state':
                                states = State.objects.filter(name__in=value['value'])
                                if value['eql'] == 'is':
                                    q |= Q(state_id__in=states)
                                elif value['eql'] == 'is_not':
                                    q |= ~Q(state_id__in=states)

                            if col == 'city':
                                cities = City.objects.filter(name__in=value['value'])
                                if value['eql'] == 'is':
                                    q |= Q(city_id__in=cities)
                                elif value['eql'] == 'is_not':
                                    q |= ~Q(city_id__in=cities)

                            if col == 'email':
                                if value['eql'] == 'are':
                                    q |= Q(email_address__in=value['value'])
                                elif value['eql'] == 'are_not':
                                    q |= ~Q(email_address__in=value['value'])

        print(q)
        recipients = Recipient.objects.filter(q)
        filters = Filter.objects.all().order_by("-created")
        filter_ = Filter.objects.get(pk=f_id)
        print(filter_)
        data = {
            'recipients': recipients,
            'filters': filters,
            'filter_': filter_,
        }
        # print(recipients)
        # return HttpResponse("check")
        return render(request, 'email_app/recipient/recipient_list.html', data)
