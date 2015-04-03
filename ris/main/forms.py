# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User as AuthUser

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory
from bootstrap3.tests import TestForm
from phonenumber_field.formfields import PhoneNumberField
import datetime

from main.models import User, Person, RadiologyRecord, PacsImage, FamilyDoctor

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


class UploadImageForm(forms.Form):
    required_css_class = 'bootstrap3-req'
    image = forms.ImageField(required=False, label='Image')


class RadiologyRecordForm(forms.ModelForm):
    required_css_class = 'bootstrap3-req'
    patient = forms.IntegerField(label='Patient ID')
    doctor = forms.IntegerField(label='Doctor ID')
    # radiologist = forms.IntegerField(label='Radiologist ID')
    test_type = forms.CharField(max_length=24, required=False)
    prescribing_date = forms.DateField(initial=datetime.date.today)
    test_date = forms.DateField(initial=datetime.date.today)
    diagnosis = forms.CharField()
    description = forms.CharField(required=False)
    # image = forms.ImageField(required=False, label='Image')
    # image = formset_factory(UploadImageForm, extra=4)

    class Meta:
        model = RadiologyRecord
        fields = ('patient', 'doctor', 'test_type', 'prescribing_date',
            'test_date', 'diagnosis', 'description')

    def clean_patient(self):
        data = self.cleaned_data.get('patient')
        if not data:
             raise forms.ValidationError("You must enter a patient id")
        try:
            data = Person.objects.get(id=data)
        except:
            raise forms.ValidationError("Patient does not exist")
        return data

    def clean_doctor(self):
        data = self.cleaned_data.get('doctor')
        if not data:
             raise forms.ValidationError("You must enter a doctor id")
        try:
            data = Person.objects.get(id=data)
        except:
            raise forms.ValidationError("Doctor does not exist")
        return data

class CreateRadiologyRecordForm(RadiologyRecordForm):
    image = forms.ImageField(required=False, label='Image')

    class Meta:
        model = RadiologyRecord
        fields = ('patient', 'doctor', 'test_type', 'prescribing_date',
            'test_date', 'diagnosis', 'description', 'image')
    #
    # def save(self, commit=True):
    #     # do something with self.cleaned_data['temp_id']
    #     patient = form.cleaned_data['patient']
    #     doctor = form.cleaned_data['doctor']
    #     radiologist = User.objects.get(auth_user__id=request.user.id).person
    #
    #     radiology_record = RadiologyRecord.objects.create(
    #         radiologist=radiologist,
    #         **form.cleaned_data)
    #
    #     # build base64 encoding for images
    #     if form.cleaned_data['image']:
    #
    #         image = form.cleaned_data['image'].read()
    #         image_b64 = base64.b64encode(image)
    #
    #         thumb = ImageOps.fit(Image.open(cStringIO.StringIO(image)), (200,200), Image.ANTIALIAS)
    #         thumb_buffer = cStringIO.StringIO()
    #         thumb.save(thumb_buffer, format="JPEG")
    #         thumb_b64 = base64.b64encode(thumb_buffer.getvalue())
    #
    #         # add pacs image to database
    #         pacs_image = PacsImage.objects.create(
    #             record=radiology_record,
    #             full_size=image_b64,
    #             thumbnail=thumb_b64
    #         )
    #     return super(PointForm, self).save(commit=commit)
