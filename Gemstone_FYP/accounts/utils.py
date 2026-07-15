import secrets
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return ''.join(str(secrets.randbelow(10)) for _ in range(6))


def send_otp_email(email, otp):
    send_mail(
        subject="Gemstone Email Verification",
        message=f"""
Hello,

Your verification code is:

{otp}

This OTP is valid for 5 minutes.

If you did not request this account, please ignore this email.

Thank you,
Gemstone Team
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )