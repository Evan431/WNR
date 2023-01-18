from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from myapp.models import User

def send_verification_email(user_email):
    """
    Sends a verification email to the specified email address with a link
    to verify the user's email address.
    """
    code = get_random_string(length=32)
    current_site = get_current_site(request)
    email_subject = 'Verify your email address'
    email_body = f'Hi,\n\nVous vous êtes récemment inscrit sur notre site. Pour finaliser votre inscription, veuillez cliquer sur ce lien : {current_site}/verification/{code}\n\nMerci'
    send_mail(email_subject, email_body, 'noreply@example.com', [user_email])
    # Save the code and the code's expiration date in the user's profile
    user = User.objects.get(email=user_email)
    user.verification_code = code
    user.verification_code_expiration = timezone.now() + timezone.timedelta(days=1)
    user.save()