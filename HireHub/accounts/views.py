from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm, CustomAuthenticationForm
from applications.models import JobApplication

# ------------------------------
# Registration View
# ------------------------------
def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

# ------------------------------
# Login View
# ------------------------------
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Remember Me
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)  # Browser close
            else:
                request.session.set_expiry(1209600)  # 2 weeks

            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# ------------------------------
# Logout View
# ------------------------------
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        request.session.flush()
        response = redirect('login')  # create response object

        # delete all cookies from the client
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)

        return response  # <-- return the response that deleted cookies

    return redirect('login')

# ------------------------------
# Dashboard/Profile
# ------------------------------
def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    applicant_email = request.user.email or request.user.username
    applications = JobApplication.objects.filter(applicant_email=applicant_email).select_related('job')

    return render(request, 'accounts/profile.html', {'applications': applications})