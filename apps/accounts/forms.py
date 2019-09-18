from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your username"
            }
    )
    )

    password=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your password"
            }
        )
        )

class RegistrationForm(forms.Form):
    username=forms.CharField(
        max_length=10,required=True, widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your username"
            }
        )
                             )
    email=forms.EmailField(
        max_length=254, required=True, widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "You email"
            }
        )

    )
    password=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your password"
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password"
            }
        )
    )

    def clean_username(self):
        username=self.cleaned_data.get('username')
        qs=User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username


    def clean_email(self):
        email=self.cleaned_data.get('email')
        qs=User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is taken")
        return email

    def clean(self):
        data=self.cleaned_data
        password1=self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 != password2:
            raise forms.ValidationError("Password must match")
        return data