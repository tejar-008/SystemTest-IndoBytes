import re
from django import forms
from app.models import User
from django.contrib.auth import password_validation


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email__iexact=email).first()
        if user:
            if not user.is_active:
                raise forms.ValidationError(
                    "This account is inactive."
                )
        return email


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)


class UserSignUpForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = User.objects.filter(username__iexact=username).first()
        if user:
            raise forms.ValidationError("This username already exists."
                                        )
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email__iexact=email).first()
        if user:
            raise forms.ValidationError(
                "This email already exists, use another email."
            )
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("Password should be minimum 8 characters long")

        if password != self.data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pat = re.compile(reg)
        password_valid = re.search(pat, password)
        if password != self.data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")
        if not password_valid:
            raise forms.ValidationError("Passwords should contain a min 8 chars, a number ,a capital letter,a small letter")
        password_validation.validate_password(
            self.cleaned_data.get('password'))
        return password


class UserCreateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = User.objects.filter(username__iexact=username).first()
        if user:
            if user.username != self.data['username']:
                raise forms.ValidationError("This username already exists."
                                            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email__iexact=email).first()
        if user:
            if user.email != self.data['email']:
                raise forms.ValidationError(
                    "This email already exists, use another email."
                )
        return email
