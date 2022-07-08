import json
from datetime import date

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.utils.timezone import now
from django.views import View
from django.views.generic import FormView, ListView, UpdateView, DetailView, DeleteView, TemplateView

from core.models import Country, State, City
from email_app.forms import EmailForm
from email_app.models import Email, History, Recipient, Filter
from django.core.mail import send_mail


# class EmailFormView(FormView):
#     form_class = EmailForm
#     # fields = ['subject', 'email_body']
#     template_name = 'email_app/email/email_form.html'
#     success_url = reverse_lazy('/success/')
#
#     # def get_initial(self):
#     #     return {'created_by': self.request.user}
#
#     def form_valid(self, form):
#         # Email.objects.create(created_by=self.request.user, subject=form.cleaned_data['subject'],
#         #                      email_body=form.cleaned_data['email_body'])
#
#         # fm = form.save(commit=False)
#         # fm.created_by = self.request.user
#         # form.save()
#
#         form.save(created_by=self.request.user)
#
#         return redirect('email-list')
#
#         # return HttpResponse("email added")

class CreateEmailForm(View):
    def get(self, request):
        return render(request, 'email_app/email/create_email_form1.html')

    def post(self, request):
        subject = request.POST.get('subject')
        body = request.POST.get('summer_html_code')
        print(f'subject : {subject}, body: {body}')
        Email.objects.create(created_by=self.request.user, subject=subject, email_body=body)
        return redirect('email-list')


class EmailListView(ListView):
    model = Email
    template_name = 'email_app/email/email_list.html'
    context_object_name = 'emails'
    ordering = ["-created"]


class EmailDetailView(DetailView):
    model = Email
    context_object_name = 'email'
    template_name = 'email_app/email/email_details.html'


# class EmailUpdateView(UpdateView):
#     model = Email
#     form_class = EmailForm
#     # fields = '__all__'
#     template_name = 'email_app/email/email_update.html'
#     success_url = '/email_list/'


class EmailUpdate(View):
    def get(self, request, pk):
        email = Email.objects.get(pk=pk)
        email_subject = email.subject
        email_body = email.email_body
        data = {
            'subject': email_subject,
            'body': email_body,
        }
        return render(request, 'email_app/email/email_update1.html', data)

    def post(self, request, pk):
        subject = request.POST.get('subject')
        body = request.POST.get('summer_html_code')
        print(f'subject : {subject}, body: {body}')
        email = Email.objects.get(pk=pk)
        email.subject = subject
        email.email_body = body
        email.save()
        return redirect("email-list")


class EmailDeleteView(DeleteView):
    model = Email
    template_name = 'email_app/email/email_confirm_delete.html'
    success_url = '/email_list/'


class EmailSuccess(TemplateView):
    template_name = 'email_app/email/email_sent_success.html'


class EmailNotSuccess(TemplateView):
    template_name = 'email_app/email/email_sent_not_success.html'


class EmailSendList(ListView):
    model = History
    template_name = 'email_app/email/email_history_list.html'
    context_object_name = 'histories'
    ordering = ["-created"]


class EmailSendDetailView(DetailView):
    model = History
    context_object_name = 'history'
    template_name = 'email_app/email/email_history_details.html'


class EmailHistoryDeleteView(DeleteView):
    model = History
    template_name = 'email_app/email/email_history_delete.html'
    success_url = '/admin/emails/'


class EmailSendRecipient(View):
    def get(self, request):
        recipients = Recipient.objects.all().order_by("-created")
        emails = Email.objects.all().order_by("-created")
        # filters = Filter.objects.all()
        data = {
            "recipients": recipients,
            "emails": emails,
            # "filters": filters,
        }
        return render(request, 'email_app/email/email_sending_recipient_input.html', data)

    def post(self, request):
        recipients = request.POST.getlist("recipients")
        subject = request.POST.get("subject")
        if recipients is not None and subject is not None:
            email = Email.objects.get(subject=subject)
            email_body = email.email_body
            arr = []
            for i in recipients:
                recipient = Recipient.objects.get(email_address=i)
                e_body = email_body.replace('{name}', recipient.name).replace('{email}', i)

                # e_body_ = e_body + f'<img src="http://127.0.0.1:8000/admin/email/tracking/{ recipient.id }/{ email.id }/" width="20px" height="20px">'

                e_body_ = e_body + f'<img src="https://sourov8251.pythonanywhere.com/admin/email/tracking/{recipient.id}/{email.id}" width="0px" height="0px">'
                print(e_body_)
                arr.append(i)
                # History.objects.create(email=i, subject=subject, body=email.email_body, created_by=self.request.user)
                send_mail(subject, e_body_, from_email='souravsarker2015@gmail.com', recipient_list=arr, html_message=e_body_)
                arr = []

        return redirect('email-send-success')


class EmailSendEmailAddress(View):
    def get(self, request):
        # recipients = Recipient.objects.all()
        emails = Email.objects.all().order_by("-created")
        # filters = Filter.objects.all()
        data = {
            # "recipients": recipients,
            "emails": emails,
            # "filters": filters,
        }
        return render(request, 'email_app/email/email_sending_email_address_input.html', data)

    def post(self, request):
        email_address = request.POST.getlist("email")
        subject = request.POST.get("subject")

        if email_address is not None and subject is not None:
            email = Email.objects.get(subject=subject)
            email_body = email.email_body
            arr = []
            for i in email_address:
                if Recipient.objects.filter(email_address=i).exists():
                    recipient = Recipient.objects.get(email_address=i)
                    e_body = email_body.replace('{email}', i).replace('{name}', recipient.name)
                    e_body_ = e_body + f'<img src="https://sourov8251.pythonanywhere.com/admin/email/tracking/{recipient.id}/{email.id}" width="0px" height="0px">'
                    print(e_body_)
                else:
                    e_body = email_body.replace('{email}', i).replace('{name}', i)
                    e_body_ = e_body + f'<img src="https://sourov8251.pythonanywhere.com/admin/email/tracking_/{i}/{email.id}" width="0px" height="0px">'

                print(e_body_)
                arr.append(i)
                # History.objects.create(email=i, subject=subject, body=email_body, created_by=self.request.user)

                send_mail(subject, e_body_, from_email='souravsarker2015@gmail.com', recipient_list=arr, html_message=e_body_)
                arr = []

        return redirect('email-send-success')


class EmailSendFilter(View):
    def get(self, request):
        emails = Email.objects.all().order_by("-created")
        filters = Filter.objects.all().order_by("-created")
        data = {
            "emails": emails,
            "filters": filters,
        }
        return render(request, 'email_app/email/email_sending_filter_input.html', data)

    def post(self, request):
        filter_ = request.POST.get("filter")
        title = request.POST.get("subject")
        filter_ = filter_.replace("\'", "\"")
        filter_list = json.loads(filter_)
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
        result = Recipient.objects.filter(q)
        # print(result)
        # print(type(result))
        # print(result.query)
        arr = []
        if result is not None and title is not None:
            print(result)
            email = Email.objects.get(subject=title)
            email_body = email.email_body
            # print(title)
            # print(email.email_body)

            for i in result:
                arr.append(i)
                recipient = Recipient.objects.get(email_address=i)
                e_body = email_body.replace('{name}', str(recipient.name)).replace('{email}', str(i))
                e_body_ = e_body + f'<img src="https://sourov8251.pythonanywhere.com/admin/email/tracking/{recipient.id}/{email.id}" width="0px" height="0px">'

                History.objects.create(email=i, subject=title, body=email.email_body, created_by=self.request.user)
                send_mail(title, e_body_, from_email='souravsarker2015@gmail.com', recipient_list=arr, html_message=e_body_)
                arr = []
            return redirect('email-send-success')
        return redirect("email-send-not-success")


class EmailSend(View):
    def get(self, request):
        recipients = Recipient.objects.all()
        emails = Email.objects.all()
        data = {
            "recipients": recipients,
            "emails": emails,
        }
        return render(request, 'email_app/email/email_send.html', data)

    def post(self, request):
        email = request.POST.get('email')
        email_list = list(email.split(','))
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        arr = []
        for i in email_list:
            arr.append(i)
            History.objects.create(email=i, subject=subject, body=body, created_by=self.request.user)
            send_mail(subject, body, from_email='souravsarker2015@gmail.com', recipient_list=arr)
            arr = []
        # return HttpResponse("got")
        return redirect('email-send-success')


class FilterEmailSend(View):
    def get(self, request):
        recipients = Recipient.objects.all().order_by("-created")
        emails = Email.objects.all().order_by("-created")
        filters = Filter.objects.all().order_by("-created")
        data = {
            "recipients": recipients,
            "emails": emails,
            "filters": filters,
        }
        return render(request, 'email_app/email/email_sending_f.html', data)

    def post(self, request):
        print(self.request.user.username)
        print(self.request.user.email)
        email_address = request.POST.getlist("email_address_input_value")
        recipients = request.POST.getlist("recipients_input_value")

        subject = request.POST.get("email_input_value")
        arr = []
        if email_address is not None and subject is not None:
            print(email_address)
            email = Email.objects.get(subject=subject)
            print(subject)
            print(email.email_body)
            for i in email_address:
                arr.append(i)
                History.objects.create(email=i, subject=subject, body=email.email_body, created_by=self.request.user)
                send_mail(subject, email.email_body, from_email='souravsarker2015@gmail.com', recipient_list=arr)
                arr = []

        if recipients is not None and subject is not None:
            email = Email.objects.get(subject=subject)
            for i in recipients:
                arr.append(i)
                History.objects.create(email=i, subject=subject, body=email.email_body, created_by=self.request.user)
                send_mail(subject, email.email_body, from_email='souravsarker2015@gmail.com', recipient_list=arr)
                arr = []

        return redirect('email-send-success')


def age_to_dob_calculate(arg):
    current = now().date()
    return date(current.year - int(arg), current.month, current.day)


def age_to_dob_calculate_minus(arg):
    current = now().date()
    return date(current.year - int(arg) - 1, current.month, current.day)


def age_to_dob_calculate_plus(arg):
    current = now().date()
    return date(current.year - int(arg) + 1, current.month, current.day)

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

# if email_address is not None and subject is not None:
#     print(email_address)
#     email = Email.objects.get(subject=subject)
#     print(subject)
#     print(email.email_body)
#     for i in email_address:
#         arr.append(i)
#         History.objects.create(email=i, subject=subject, body=email.email_body, created_by=self.request.user)
#         send_mail(subject, email.email_body, from_email='souravsarker2015@gmail.com', recipient_list=arr)
# arr = []


# if recipients is not None and subject is not None:
#     email = Email.objects.get(subject=subject)
#     # arr = []
#     for i in recipients:
#         arr.append(i)
#         History.objects.create(email=i, subject=subject, body=email.email_body, created_by=self.request.user)
#         send_mail(subject, email.email_body, from_email='souravsarker2015@gmail.com', recipient_list=arr)
#         arr = []


# query_json = {
#     "age": {"value": 10, "condition": "is"},
#     "country": {"value": ["United States", "United Kingdom"], "condition": "is"}
# }

# query = Q()
# if query_json.get("age") is not None:
#     if query_json.get("age").get("condition") is "is":
#         query &= Q(age='age')
#     elif query_json.get("age").get("condition") is "is not":
#         query &= Q(name='age')
# if query_json.get("country") is not None:
#     if query_json.get("country").get("condition") is "is":
#         query &= Q(name='country')

# history = History.objects.filter(query)


# print(type(query_json))

# for value in query_list:
#     # print(value['col'])
#     if isinstance(value, dict):
#         print(value['value'])
#         if value['value'] != '':
#             print('inner')
# query_json = json.dumps(query_json)
# print(query_json)
# print(type(query_json))
# q = Q()

# recipients = Recipient.objects.all()
# for i in recipients:
#     print(i)
# recipients = Recipient.objects.get(age__gt=24)
# print(recipients)

# if query_json.get("country").get("value") is not None:
#     print('inter')
#     if query_json.get("country").get("eql") == "is":
#         print(query_json.get("country").get("value"))
#         for i in query_json.get("country").get("value"):
#             query &= Q(country=i)
# print(query_json.get("age").get("value"))

# print(query)
# recipients = Recipient.objects.filter(country__in=query)
# print(recipients)

# return HttpResponse("check")
# for i in email_address:
#     arr.append(i)
#     History.objects.create(email=i, subject=subject, body=email.email_body, created_by=self.request.user)
#     send_mail(subject, email.email_body, from_email='souravsarker2015@gmail.com', recipient_list=arr)
#     arr = []

# print(recipients.query)
# if query_json.age is not None:
# print(query_json.age)
# query = Q()
# if query_json.get("age") is not None:
#     if query_json.get("age").get("condition") is "is":
#         query &= Q(age='age')
#     elif query_json.get("age").get("condition") is "is not":
#         query &= Q(name='age')
# if query_json.get("country") is not None:
#     if query_json.get("country").get("condition") is "is":
#         query &= Q(name='country')

# history = History.objects.filter(query)
# print(query_json)
# arr = []
# if filter_ is not None and title is not None:
#
#     filter_ = Filter.objects.get(title=title)
#     print(title)
#     print(filter_.content)


# if query_json.get("age").get("value") is not None:
#     print('inter')
#     if query_json.get("age").get("eql") == "is":
#         query &= Q(age="age")
#         print('inter')
#     # print(query_json.get("age").get("value"))

# def send_email(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         email = list(email.split(','))
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#         print(email, subject, message)
#         send_mail(subject, message, from_email='souravsarker2015@gmail.com', recipient_list=email)
#         return HttpResponse("got")
#     return render(request, 'email_app/email/email_send.html')
