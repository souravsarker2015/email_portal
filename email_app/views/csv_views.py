import csv
from dateutil import parser
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from core.models import Country, State, City
from email_app.forms import CsvForm
from email_app.models import Csv, Recipient
import datetime

# datetime.datetime.strptime('5/10/1955', '%d/%m/%Y').strftime('%Y-%m-%d')

from django.conf import settings


class CsvFileView(View):
    def get(self, request):
        form = CsvForm(request.POST or None, request.FILES or None)
        return render(request, "email_app/csv/csv_template.html", {'form': form})

    def post(self, request):
        form = CsvForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            obj = Csv.objects.get(activated=False)
            with open(obj.file_name.path, 'r') as f:
                reader = csv.reader(f)
                recipients_email_address_list = list(Recipient.objects.values('email_address'))
                arr = []
                for i in recipients_email_address_list:
                    for k, v in i.items():
                        arr.append(v)

                for i, row in enumerate(reader):
                    if i == 0:
                        pass
                    else:
                        name = row[0]
                        email_address = row[1]
                        country = Country.objects.get(Q(name__icontains=row[2]) | Q(code__icontains=row[2]))
                        # country = int(row[2])
                        state = State.objects.get(name__icontains=row[3])
                        city = City.objects.get(name__icontains=row[4])
                        dob = parser.parse(row[5])
                        print(dob)
                        if email_address not in arr:
                            Recipient.objects.create(name=name, email_address=email_address, country_id=country.id, state_id=state.id, city_id=city.id, dob=dob)

                obj.activated = True
                obj.save()
        return redirect("recipient-list")
