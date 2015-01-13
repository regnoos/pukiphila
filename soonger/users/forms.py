from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm

from .models import User


class UserCreationForm(DjangoUserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control input-lg text-center no-border',
            'placeholder': 'Username',
            'autocomplete': 'off',
            'autofocus': 'autofocus'}),
        error_messages={'unique': 'Please enter your name'})

    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={
            'class': 'form-control input-lg text-center no-border',
            'placeholder': 'Email',
            'autocomplete': 'off'}))

    password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control input-lg text-center no-border',
            'placeholder': 'Password',
            'autocomplete': 'off'}))

    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control input-lg text-center no-border',
            'placeholder': 'Re-type Your Password',
            'autocomplete': 'off'}))

    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=((u'M', 'Hombre'), (u'F', 'Mujer'),))

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'gender',)


class UserChangeForm(DjangoUserChangeForm):

    class Meta:
        model = User
        fields = '__all__'