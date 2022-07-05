import json
from json import dumps

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from core.models import Country, State, City
from email_app.models import Email, Recipient, Filter


class FilterView(View):
    def get(self, request):
        country = Country.objects.all()
        state = State.objects.all()
        city = City.objects.all()
        emails = Email.objects.all()
        recipients = Recipient.objects.all()
        data = {
            'country': country,
            'state': state,
            'city': city,
            'emails': emails,
            'recipients': recipients,
        }
        return render(request, 'email_app/filter/filter9.html', data)

    def post(self, request):
        title = request.POST.get('title')
        print(title)
        query_json = []
        if request.POST.get('age_value') is not None:
            query_json.append({
                "op": "",
                "col": request.POST.get("age_col"),
                "eql": request.POST.get("age_eql", "is"),
                "value": request.POST.get("age_value", "0"),
            })

        if request.POST.get('country_value') is not None:
            query_json.append({
                "op": request.POST.get("country_op", ""),
                "col": request.POST.get("country_col"),
                "eql": request.POST.get("country_eql", "is"),
                "value": request.POST.getlist("country_value"),
            })

        if request.POST.get('state_value') is not None:
            query_json.append({
                "op": request.POST.get("state_op", ""),
                "col": request.POST.get("state_col"),
                "eql": request.POST.get("state_eql", "is"),
                "value": request.POST.getlist("state_value"),
            })

        if request.POST.get('city_value') is not None:
            query_json.append({
                "op": request.POST.get("city_op", ""),
                "col": request.POST.get("city_col"),
                "eql": request.POST.get("city_eql", "is"),
                "value": request.POST.getlist("city_value"),
            })

        if request.POST.get('email_value') is not None:
            query_json.append({
                "op": request.POST.get("email_op", ""),
                "col": request.POST.get("email_col"),
                "eql": request.POST.get("email_eql", "are"),
                "value": request.POST.getlist("email_value"),
            })

        value = json.dumps(query_json)
        Filter.objects.create(title=title, content=query_json, created_by=self.request.user)
        print(value)
        print(type(value))
        print(query_json)
        print(type(query_json))
        # return HttpResponse("check")
        return redirect('filter-list')


class FilterListView(ListView):
    model = Filter
    template_name = 'email_app/filter/filter_list.html'
    context_object_name = 'filters'
    ordering = ["-created"]


class FilterDetailView(DetailView):
    model = Filter
    context_object_name = 'filter'
    template_name = 'email_app/filter/filter_detail.html'


class FilterDeleteView(DeleteView):
    model = Filter
    template_name = 'email_app/filter/filter_delete.html'
    success_url = '/filter_list/'

# class FilterUpdateView(UpdateView):
#     model = Email
#     form_class = EmailForm
#     # fields = '__all__'
#     template_name = 'email_app/email/email_update.html'
#     success_url = '/email_list/'
# def send_dictionary(request):
#     # create data dictionary
#     dataDictionary = {
#         'hello': 'World',
#         'geeks': 'forgeeks',
#         'ABC': 123,
#         456: 'abc',
#         14000605: 1,
#         'list': ['geeks', 4, 'geeks'],
#         'dictionary': {'you': 'can', 'send': 'anything', 3: 1}
#     }
#     # dump data
#     dataJSON = dumps(dataDictionary)
#     return render(request, 'email_app/test/test.html', {'data': dataJSON})

# query_json = {}
# if request.POST.get("age_value") is not None:
#     query_json["age"] = {
#         "value": int(request.POST.get("age_value", "0")),
#         "condition": request.POST.get("age_condition", "is"),
#     }
# if request.POST.get("country_value") is not None:
#     query_json["country"] = {
#         "value": request.POST.getlist('country_value'),
#         "condition": request.POST.get("country_condition", "is"),
#     }
# value = json.dumps(query_json)


# age = request.POST.get('age_select')
# age_condition = request.POST.get('age_condition')
# age_value = request.POST.get('age_value')
# print(f"{age} || {age_condition} || {age_value}")
#
# country_and_or = request.POST.get('country_and_or')
# country = request.POST.get('country_select')
# country_is_is_not = request.POST.get('country_is_is_not')
# country_value = request.POST.getlist('country_value')
# print(f"{country_and_or} || {country} || {country_is_is_not} || {country_value}")
#
# state_and_or = request.POST.get('state_and_or')
# state = request.POST.get('state_select')
# state_is_is_not = request.POST.get('state_is_is_not')
# state_value = request.POST.getlist('state_value')
# print(f"{state_and_or} || {state} || {state_is_is_not} || {state_value}")
#
# city_and_or = request.POST.get('city_and_or')
# city = request.POST.get('city_select')
# city_is_is_not = request.POST.get('city_is_is_not')
# city_value = request.POST.getlist('city_value')
# print(f"{city_and_or} || {city} || {city_is_is_not} || {city_value}")
#
# email_and_or = request.POST.get('email_and_or')
# email = request.POST.get('email_select')
# email_are_are_not = request.POST.get('email_are_are_not')
# email_value = request.POST.getlist('email_value')
# print(f"{email_and_or} || {email} || {email_are_are_not} || {email_value}")
