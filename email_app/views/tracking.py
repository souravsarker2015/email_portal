from django.utils.translation import override
import json
import os
from django.http import HttpResponse

from email_app.models import Email, Recipient


def email_seen(request, r_id, e_id):
    r = Recipient.objects.get(id=r_id)
    e = Email.objects.get(id=e_id)
    print("Successfully Tracked")
    print(f"recipient name: {r.name}")
    print(f"email sub: {e.subject}")

    return HttpResponse("check")
    # with open(os.path.dirname(os.path.abspath(__file__)) + "/10.png", "rb") as f:
    #     return HttpResponse(f.read(), content_type="image/png")

# from django.utils.timezone import now
# from django.utils.translation import override
# import json
# import os
# from django.http import HttpResponse
# from django.views import View

# from email_app.models import Email
# import os.path
#
#
# class PixelView(View):
#
#     def get(self, request, *args, **kwargs):
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         image_data = open(os.path.join(script_dir, 'static/res/1x1.png'), 'rb').read()
#         user_id = kwargs.get('user')
#         print("tracked")
#         return HttpResponse(image_data, content_type="image/png")

#
# def email_seen(request, key):
#     META = {
#         header: value
#         for header, value in request.META.items()
#         if header.startswith(("HTTP_", "REMOTE_"))
#     }
#     Email.objects.filter(key=key, seen_at=None).update(
#         request=json.dumps(META), seen_at=now()
#     )
#     print("Successfully Tracked")
#     with open(os.path.dirname(os.path.abspath(__file__)) + "static/res/1x1.png", "rb") as f:
#         return HttpResponse(f.read(), content_type="image/png")

# import http
#
# from django.http import HttpResponse
#
# from email_app.models import Recipient, Email
#
#
# def email_seen_(request, r_id):
#     if 'r_id' in request.GET:
#         # do something with the id, which tells you that specific subscriber has opened the email.
#         # do something to record that an email has been opened.
#         image_data = open("static/img/log.webp", 'rb').read()
#         return HttpResponse(image_data, mimetype="image/png")

# from django.utils.timezone import now
# from django.utils.translation import override
# import json
# import os
# from django.http import HttpResponse
#
# from email_app.models import YourModel
#
#
# def email_seen(request, key):
#     META = {
#         header: value
#         for header, value in request.META.items()
#         if header.startswith(("HTTP_", "REMOTE_"))
#     }
#     YourModel.objects.filter(key=key, seen_at=None).update(
#         request=json.dumps(META), seen_at=now()
#     )
#     print("Successfully Tracketd")
#     with open(os.path.dirname(os.path.abspath(__file__)) + "", "rb") as f:
#         return HttpResponse(f.read(), content_type="image/png")
