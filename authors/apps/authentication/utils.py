import os
from django.core.mail import send_mail


def send_password_reset_email(to_email, token, call_back_url):
    # current_site = os.environ.get("CURRENT_SITE")
    # email setup
    subject = 'Password reset'
    message = """
                    You're receiving this email because you invoked a password reset on
                    Authors haven. If you think it is a mistake to receive this email just ignore it.

                    ----- Click the link below to reset your password ----
                        {}?{}

                   """.format(call_back_url, token)
    from_email = os.environ.get('EMAIL_HOST_USER')
    to_email = to_email
    try:
        send_mail(subject, message, from_email, [to_email], fail_silently=False, )
    except Exception as e:
        return {'email': str(e)}