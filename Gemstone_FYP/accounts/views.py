from .forms import SignUpForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.views import View
from .models import EmailOTP
from .utils import generate_otp, send_otp_email
from .forms import OTPVerificationForm

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(View):
    template_name = "accounts/signup.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            if EmailOTP.objects.filter(email=email).exists():
                EmailOTP.objects.filter(email=email).delete()

            otp = generate_otp()

            EmailOTP.objects.update_or_create(
                email=email,
                defaults={
                    "otp": otp,
                    "resend_count": 1,
                }
            )

            send_otp_email(email, otp)

            request.session["signup_data"] = {
                "username": form.cleaned_data["username"],
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "email": email,
                "phone": form.cleaned_data["phone"],
                "address": form.cleaned_data["address"],
                "password": form.cleaned_data["password1"],
            }

            messages.success(request, "OTP sent successfully.")

            return redirect("verify_otp")

        return render(request, self.template_name, {"form": form})


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("profile")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")


class CustomPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset_form.html"
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


class VerifyOTPView(View):

    template_name = "accounts/verify_otp.html"

    def get(self, request):
        form = OTPVerificationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = OTPVerificationForm(request.POST)

        if form.is_valid():

            entered_otp = form.cleaned_data["otp"]

            signup_data = request.session.get("signup_data")

            if not signup_data:
                messages.error(request, "Session expired. Please register again.")
                return redirect("signup")

            email = signup_data["email"]

            otp_obj = get_object_or_404(EmailOTP, email=email)

            if otp_obj.is_expired():
                otp_obj.delete()
                messages.error(request, "OTP has expired.")
                return redirect("signup")

            if otp_obj.otp != entered_otp:
                messages.error(request, "Invalid OTP.")
                return render(request, self.template_name, {"form": form})

            user = User.objects.create_user(
                username=signup_data["username"],
                first_name=signup_data["first_name"],
                last_name=signup_data["last_name"],
                email=signup_data["email"],
                phone=signup_data["phone"],
                address=signup_data["address"],
                password=signup_data["password"],
            )

            login(request, user)

            otp_obj.delete()

            request.session.pop("signup_data", None)

            messages.success(request, "Account created successfully!")

            return redirect("congrats")

        return render(request, self.template_name, {"form": form})

from django.utils import timezone

class ResendOTPView(View):

    def post(self, request):

        signup_data = request.session.get("signup_data")

        if not signup_data:
            messages.error(request, "Session expired. Please register again.")
            return redirect("signup")

        email = signup_data["email"]

        otp_obj = EmailOTP.objects.get(email=email)

        # Maximum 3 OTPs (1 original + 2 resends)
        if otp_obj.resend_count >= 3:
            messages.error(request, "You have reached the maximum number of OTP requests.")
            return redirect("verify_otp")

        otp = generate_otp()

        otp_obj.otp = otp
        otp_obj.resend_count += 1
        otp_obj.created_at = timezone.now()   # Reset expiry
        otp_obj.save()

        send_otp_email(email, otp)

        messages.success(request, "A new OTP has been sent to your email.")

        return redirect("verify_otp")