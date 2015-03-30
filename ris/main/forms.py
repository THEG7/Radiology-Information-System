# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User as AuthUser

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory
from bootstrap3.tests import TestForm
from phonenumber_field.formfields import PhoneNumberField

from main.models import User, Person

CLASS_CHOICES = (
    ('p', 'Patient'),
    ('d', 'Doctor'),
    ('r', 'Radiologist'),
)

class LoginForm(forms.Form):
    required_css_class = 'bootstrap3-req'
    username = forms.CharField(
        max_length=16,
        help_text='<i>must be at least 5 characters long</i>',
        label='Username')
    password = forms.CharField(widget=forms.PasswordInput, min_length=5, max_length=128)


class AuthUserForm(forms.ModelForm):
    required_css_class = 'bootstrap3-req'
    username = forms.CharField(
        max_length=16,
        label='Username')
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=5,
        max_length=128,
        help_text='<i>must be at least 5 characters long</i>')

    class Meta:
        model = AuthUser
        fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):
    required_css_class = 'bootstrap3-req'
    class_field = forms.ChoiceField(choices=CLASS_CHOICES)

    class Meta:
        model = User
        fields = ('class_field',)


class PersonForm(forms.ModelForm):
    required_css_class = 'bootstrap3-req'
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    address = forms.CharField(max_length=128, required=False)
    email = forms.EmailField(max_length=128)
    phone = PhoneNumberField(
        required=False,
        max_length=14,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. +17801234567'})
    )

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'address', 'email', 'phone')


class UploadForm(forms.Form):
    text1 = forms.CharField()
    file1 = forms.FileField()
    file2 = forms.FileField(required=False)
    file3 = forms.FileField(widget=forms.ClearableFileInput)
    file4 = forms.FileField(required=False, widget=forms.ClearableFileInput)


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data
