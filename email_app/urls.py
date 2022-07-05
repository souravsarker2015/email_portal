from django.urls import path
from email_app import views as email_app_views
from .cron import mail_schedule, mail_schedule_view
from .forms import LoginForm
from django.contrib.auth import views as auth_view
from django.contrib.auth.decorators import login_required
from .views import email_views as email_views, filter_views as filter_views, recipient_views as recipient_views
from email_app.views import views
from .views.csv_views import CsvFileView
from .views.schedule_views import ScheduleViews, ScheduleUpdateView, ScheduleDetailView, ScheduleDeleteView, ScheduleListView
from django.urls import path, re_path as url

# from .views.tracking import email_seen_
from .views.tracking import email_seen

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('success/', views.success_message, name='success'),

    path('recipient_list/', login_required(recipient_views.RecipientListView.as_view()), name='recipient-list'),
    path('recipient_details/<int:pk>/', login_required(recipient_views.RecipientDetailView.as_view()),
         name='recipient-details'),
    path('recipient_update/<int:pk>/', login_required(recipient_views.RecipientUpdateView.as_view()),
         name='recipient-update'),
    path('recipient_delete/<int:pk>/', login_required(recipient_views.RecipientDeleteView.as_view()),
         name='recipient-delete'),
    path('add_recipient/', login_required(recipient_views.RecipientFormView.as_view()), name='add-recipient'),

    path('add_recipient_filter/', login_required(recipient_views.RecipientFilter.as_view()),
         name='add-recipient-filter'),
    path('recipient_upload/', login_required(CsvFileView.as_view()),
         name='recipient-upload'),

    path('add_email/', login_required(email_views.CreateEmailForm.as_view()), name='add-email'),
    # path('add_email/', login_required(email_views.EmailFormView.as_view()), name='add-email'),
    path('email_list/', login_required(email_views.EmailListView.as_view()), name='email-list'),
    path('email_details/<int:pk>/', login_required(email_views.EmailDetailView.as_view()), name='email-details'),
    path('email_update/<int:pk>/', login_required(email_views.EmailUpdateView.as_view()), name='email-update'),
    path('email_delete/<int:pk>/', login_required(email_views.EmailDeleteView.as_view()), name='email-delete'),

    # path('email_send/', email_views.send_email, name='email-send'),
    path('email_send/', email_views.EmailSend.as_view(), name='email-send'),
    path('email_send_with_filter/', email_views.FilterEmailSend.as_view(), name='filter-email-send'),

    path('email_send_email_address', email_views.EmailSendEmailAddress.as_view(), name='email-send-email-address'),
    path('email_send_filter', email_views.EmailSendFilter.as_view(), name='email-send-filter'),
    path('email_send_recipient', email_views.EmailSendRecipient.as_view(), name='email-send-recipient'),

    path('email_send_list/', email_views.EmailSendList.as_view(), name='email-send-list'),
    path('email_send_detail/<int:pk>', email_views.EmailSendDetailView.as_view(), name='email-send-details'),
    path('email_send_success/', email_views.EmailSuccess.as_view(), name='email-send-success'),
    path('email_send_not_success/', email_views.EmailNotSuccess.as_view(), name='email-send-not-success'),
    path('email_history_delete/<int:pk>/', login_required(email_views.EmailHistoryDeleteView.as_view()),
         name='email-history-delete'),

    path('filter/', login_required(filter_views.FilterView.as_view()), name='add-filter'),
    path('filter_list/', login_required(filter_views.FilterListView.as_view()), name='filter-list'),
    path('filter_details/<int:pk>/', login_required(filter_views.FilterDetailView.as_view()), name='filter-details'),
    path('filter_delete/<int:pk>/', login_required(filter_views.FilterDeleteView.as_view()), name='filter-delete'),

    path('add_schedule/', login_required(ScheduleViews.as_view()), name='add-schedule'),
    path('schedule_list/', login_required(ScheduleListView.as_view()), name='schedule-list'),
    path('schedule_details/<int:pk>/', login_required(ScheduleDetailView.as_view()),
         name='schedule-details'),
    path('schedule_update/<int:pk>/', login_required(ScheduleUpdateView.as_view()),
         name='schedule-update'),
    path('schedule_delete/<int:pk>/', login_required(ScheduleDeleteView.as_view()),
         name='schedule-delete'),
    # path('test/', email_views.send_dictionary, name='test'),
    path('mail_schedule/', mail_schedule_view, name='mail-schedule'),
    path('te/', mail_schedule, name='mail_schedule'),
    path('email_tracking/<int:r_id>/<int:e_id>/', email_seen, name="email_seen"),
    # url(r"^email/tr-(?P<key>.*)\.png$", email_seen, name="email_seen"),
    # url(r"^email/tr-(?P<key>.*)\.png$", email_seen, name="email_seen"),
    # url(r"^open-tracking/(?P<user>[0-9]+)/$", PixelView.as_view(), name="pixel_view"),

    path('account/login/', auth_view.LoginView.as_view(template_name='email_app/account/login.html', authentication_form=LoginForm), name='login'),
    path('account/logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
]
