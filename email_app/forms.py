from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField
from django.forms import DateTimeInput
from django.utils.translation import gettext, gettext_lazy as _
from .models import User, Recipient, Email, Csv, Schedule
from core.models import Country, State, City


# from django.forms.widgets import DateTimeWidget

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['name', 'email_address', 'country', 'state', 'city', 'dob']
        country = forms.ModelChoiceField(queryset=Country.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}))
        state = forms.ModelChoiceField(queryset=State.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
        city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(format=('%Y-%m-%d'),
                                   attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'})
        }


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['subject', 'email_body']

        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'email_body': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'cols': '5'}),
        }

    def save(self, commit=True, created_by=None):
        instance = super(EmailForm, self).save(commit=False)
        instance.created_by = created_by

        if commit:
            instance.save()
        return instance


# class EmailForm(forms.ModelForm):
#     class Meta:
#         model = Email
#         fields = ['created_by', 'subject', 'email_body']
#         # created_by = forms.ModelChoiceField(queryset=User.objects.all(),
#         #                                     widget=forms.HiddenInput(), required=False)
#         created_by = forms.ModelChoiceField(widget=forms.HiddenInput(), label='', queryset=User.objects.all())
#         widgets = {
#             'created_by': forms.HiddenInput(),
#             'subject': forms.TextInput(attrs={'class': 'form-control'}),
#             'email_body': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'cols': '5'}),
#         }

# def save(self, commit=True, user=None, author=None):
#     user_author = super(ReviewFollowAuthorForm, self).save(commit=False)
#     user_author.user = user
#     user_author.author = author
#     if commit:
#         user_author.save()
#     return user_author


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'id': 'exampleInputEmail', 'autofocus': True,
               'placeholder': "Enter Email Address..."}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control form-control-user', 'id': "exampleInputPassword", 'placeholder': "Password"}),
    )


class CsvForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ['file_name', ]


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ["schedule_title", "date_time"]

        widgets = {
            'schedule_title': forms.TextInput(attrs={'class': 'form-control'}),
            'date_time': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
