from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import StudentProfile

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "email"]


class AvatarForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["avatar"]


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))


class PasswordResetConfirmForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter OTP"})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter new password"})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm new password"})
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("new_password1") != cleaned.get("new_password2"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned
