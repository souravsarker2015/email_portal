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

