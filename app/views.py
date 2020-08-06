import re
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from app.models import User
from django.contrib.auth import authenticate, login, logout
from app.forms import UserLoginForm, UserSignUpForm, UserCreateForm, ChangePasswordForm
from app.access_decorators_mixins import admin_login_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template import loader
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.urls import reverse


def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("app:login")
    user_count = User.objects.count()
    return render(request, "dashboard.html", {"user_count": user_count}, status=200)


def user_profile(request):
    if not request.user.is_authenticated:
        return redirect("app:login")
    user_count = User.objects.count()
    return render(request, "profile.html", {"user_count": user_count}, status=200)


def user_signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {})

    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                email=form.cleaned_data.get("email"),
                username=form.cleaned_data.get("username"),
            )
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            login(request, user)
            return redirect("app:dashboard")
        else:
            return render(
                request, "signup.html", {"errors": form.errors}
            )


def user_logout(request):
    logout(request)
    return redirect("app:login")


@admin_login_required
def user_activate(request, pk):
    user = User.objects.get(id=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect("app:user_admin")


@admin_login_required
def user_update(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        form = UserCreateForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:user_admin")
        else:
            return render(request, "admin/user_update.html",
                          {"errors": form.errors, "user": user})
    return render(
        request, "admin/user_update.html", {"user": user})


@admin_login_required
def user_delete(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect(reverse(
        "app:user_admin"))


@admin_login_required
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user_object = form.save()
            c = {
                'email': user_object.email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'User Directory',
                'uid': urlsafe_base64_encode(force_bytes(user_object.pk)),
                'user': user_object,
                'token': default_token_generator.make_token(user_object),
                'protocol': 'http',
            }
            subject_template_name = 'registration/set_password_subject.txt'
            email_template_name = 'registration/set_password_email.html'
            subject = loader.render_to_string(subject_template_name, c)
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [
                      user_object.email], fail_silently=False)
            return redirect("app:user_admin")
        else:
            return render(request, "admin/user_create.html",
                          {"errors": form.errors})
    return render(request, "admin/user_create.html")


@admin_login_required
def user_admin(request):
    users = User.objects.all()
    return render(
        request, "admin/admin.html", {"users": users})


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email__iexact=email, is_active=False)
        if user:
            return render(request, "reset-page.html", {"error": "User is deactivted"})
        if not user:
            return render(request, "reset-page.html", {"error": "Email doesnot exists"})
    return render(request, "reset-page.html")


def user_login(request):
    if request.method == "GET":
        return render(request, "login.html", {})

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is None:
                return render(
                    request,
                    "login.html",
                    {"errors": {"account_error": ["Invalid email or password"]}},
                )

            elif user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("app:dashboard")
                else:
                    return render(
                        request,
                        "login.html",
                        {
                            "errors": {
                                "account_error": ["User is inactive."]
                            }
                        },
                    )
            else:
                pass
        else:
            return render(request, "login.html", {"errors": form.errors})


@login_required
def change_password(request):
    if request.method == "GET":
        return render(request, "change_password.html", {})

    if request.method == "POST":
        user = request.user
        errors = {}
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get("old_password")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
            check_password = user.check_password(old_password)
            if not check_password:
                errors['old_password'] = "old password Doesnot match"

            if password != confirm_password:
                errors["confirm_password"] = "Passwords do not match"
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            pat = re.compile(reg)
            password_valid = re.search(pat, password)
            if not password_valid:
                errors["password"] = "Passwords should contain a min 8 chars, a number ,a capital letter,a small letter"

            if errors:
                return render(
                    request,
                    "change_password.html",
                    {"errors": errors},
                )
            user.set_password(password)
            user.save()
            return redirect("app:dashboard")
        return render(request, "change_password.html", {"errors": form.errors})
