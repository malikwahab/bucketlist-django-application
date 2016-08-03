from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    error_css_class = "Error"

    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'username',
                               }))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'password'
                               }))


class SignUpForm(forms.Form):
    error_css_class = "Error"

    username = forms.CharField(label='Username', max_length=300,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Username',
                                   'autocomplete': 'off'
                               }))
    email = forms.EmailField(label='Email', max_length=100,
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'Email',
                                 'autocomplete': 'off'
                             }))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'Password'
                               }))
    confirm_password = forms.CharField(label='Verify Password', max_length=100,
                                       widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Confirm Password'}))

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(
            "Username already exist, please choose another username")

    def clean(self):
        if 'password' in self.cleaned_data and ('confirm_password'
                                                in self.cleaned_data):
            if self.cleaned_data['password'] != self.cleaned_data['confirm_'
                                                                  'password']:
                raise forms.ValidationError(
                    "Your password doesnot match")
        return self.cleaned_data

    def save(self):
        new_user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        return new_user
