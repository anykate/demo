from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)

User = get_user_model()


class MyUserLoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control mt-5',
            'autofocus': '',
            'style': 'width:66ch',
            'placeholder': 'Enter username...',
        }
    ), )

    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter password...',
        }
    ), )

    # https://docs.djangoproject.com/en/2.1/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(
                    'Oh! I can\'t find that user - create user first!')
            elif not user.check_password(password):
                raise forms.ValidationError(
                    'Oh! That password is incorrect - try again!')
            elif not user.is_active:
                raise forms.ValidationError(
                    'Oh! That user is not active in the database!')


class MyUserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control mt-5',
            'autofocus': '',
            'style': 'width:66ch',
            'placeholder': 'Enter username...',
        }
    ), )
    email1 = forms.EmailField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Email Address...',
        }
    ), )
    email2 = forms.EmailField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Email Address...',
        }
    ), )
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter password...',
        }
    ), )

    class Meta:
        model = User
        fields = ['username', 'email1', 'email2', 'password', ]

    # https://docs.djangoproject.com/en/2.1/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
    def clean(self):
        super().clean()
        email1 = self.cleaned_data.get('email1')
        email2 = self.cleaned_data.get('email2')
        if email1 != email2:
            raise forms.ValidationError('Email addresses must match!')
        email_qs = User.objects.filter(email=email1)
        if email_qs.exists():
            raise forms.ValidationError('Email address already registered!')
