from .cron import mail_schedule, mail_schedule_view
from .forms import LoginForm
from django.contrib.auth import views as auth_view
from django.contrib.auth.decorators import login_required
from .views import email_views as email_views, filter_views as filter_views, recipient_views as recipient_views
from email_app.views import views
from .views.csv_views import CsvFileView
from .views.schedule_views import ScheduleViews, ScheduleUpdateView, ScheduleDetailView, ScheduleDeleteView, ScheduleListView, ScheduleCreated
from django.urls import path

from .views.tracking import email_seen, TrackedRecipientListView, TrackedRecipientDetailView, TrackedRecipientDeleteView, email_seen_, test2

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('success/', views.success_message, name='success'),

    path('admin/recipients/', login_required(recipient_views.RecipientListView.as_view()), name='recipient-list'),
    path('admin/recipient/<int:pk>/', login_required(recipient_views.RecipientDetailView.as_view()),
         name='recipient-details'),
    path('admin/recipient/<int:pk>/update/', login_required(recipient_views.RecipientUpdateView.as_view()),
         name='recipient-update'),
    path('admin/recipient/<int:pk>/delete/', login_required(recipient_views.RecipientDeleteView.as_view()),
         name='recipient-delete'),
    path('admin/recipient/add/', login_required(recipient_views.RecipientFormView.as_view()), name='add-recipient'),

    path('admin/filter/add', login_required(recipient_views.RecipientFilter.as_view()),
         name='add-recipient-filter'),
    path('admin/recipients/upload/', login_required(CsvFileView.as_view()),
         name='recipient-upload'),

    path('admin/email/add/', login_required(email_views.CreateEmailForm.as_view()), name='add-email'),
    # path('add_email/', login_required(email_views.EmailFormView.as_view()), name='add-email'),
    path('admin/emails/', login_required(email_views.EmailListView.as_view()), name='email-list'),
    path('admin/email/<int:pk>/', login_required(email_views.EmailDetailView.as_view()), name='email-details'),
    # path('admin/email/<int:pk>/update/', login_required(email_views.EmailUpdateView.as_view()), name='email-update_'),

    path('admin/email/<int:pk>/update/', login_required(email_views.EmailUpdate.as_view()), name='email-update'),
    path('admin/email/<int:pk>/delete/', login_required(email_views.EmailDeleteView.as_view()), name='email-delete'),

    # path('email_send/', email_views.send_email, name='email-send'),
    path('email-send/', email_views.EmailSend.as_view(), name='email-send'),
    path('email/send/options/', email_views.FilterEmailSend.as_view(), name='filter-email-send'),

    path('email/send/email-address/', email_views.EmailSendEmailAddress.as_view(), name='email-send-email-address'),
    path('email/send/filter/', email_views.EmailSendFilter.as_view(), name='email-send-filter'),
    path('email/send/recipients/', email_views.EmailSendRecipient.as_view(), name='email-send-recipient'),

    path('admin/email/histories/', email_views.EmailSendList.as_view(), name='email-send-list'),
    path('admin/email/history/<int:pk>/', email_views.EmailSendDetailView.as_view(), name='email-send-details'),
    path('admin/email/success/', email_views.EmailSuccess.as_view(), name='email-send-success'),
    path('admin/email/send/not-success/', email_views.EmailNotSuccess.as_view(), name='email-send-not-success'),
    path('admin/history/<int:pk>/delete/', login_required(email_views.EmailHistoryDeleteView.as_view()),
         name='email-history-delete'),

    path('admin/filter/add/', login_required(filter_views.FilterView.as_view()), name='add-filter'),
    path('admin/filters/', login_required(filter_views.FilterListView.as_view()), name='filter-list'),
    path('admin/filter/<int:pk>/', login_required(filter_views.FilterDetailView.as_view()), name='filter-details'),
    path('admin/filter/<int:pk>/delete/', login_required(filter_views.FilterDeleteView.as_view()), name='filter-delete'),

    path('admin/schedule/add/', login_required(ScheduleViews.as_view()), name='add-schedule'),
    path('admin/schedules/', login_required(ScheduleListView.as_view()), name='schedule-list'),
    path('admin/schedule/<int:pk>/', login_required(ScheduleDetailView.as_view()),
         name='schedule-details'),
    path('admin/schedule/<int:pk>/update/', login_required(ScheduleUpdateView.as_view()),
         name='schedule-update'),
    path('admin/schedule/<int:pk>/delete/', login_required(ScheduleDeleteView.as_view()),
         name='schedule-delete'),
    path('email/schedule/', mail_schedule_view, name='mail-schedule'),
    path('schedule/created/', ScheduleCreated.as_view(), name='schedule-created'),

    path('admin/tracked/recipients/', login_required(TrackedRecipientListView.as_view()), name='tracked-recipients-list'),
    path('admin/tracked/recipient/<int:pk>/', login_required(TrackedRecipientDetailView.as_view()), name='tracked-recipients-details'),
    path('admin/tracked/recipient/<int:pk>/delete/', login_required(TrackedRecipientDeleteView.as_view()), name='tracked-recipients-delete'),

    path('te/', mail_schedule, name='mail_schedule'),
    path('admin/email/tracking/<int:r_id>/<int:e_id>', email_seen, name="email_seen"),
    path('admin/email/tracking_/<str:r_email>/<int:e_id>', email_seen_, name="email_seen"),
    path('test/', test2, name="test2"),

    path('account/login/', auth_view.LoginView.as_view(template_name='email_app/account/login.html', authentication_form=LoginForm), name='login'),
    path('account/logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
]
