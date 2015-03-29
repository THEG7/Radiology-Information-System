from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import datetime


class Person(models.Model):
    person_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=24, blank=True)
    last_name = models.CharField(max_length=24, blank=True)
    address = models.CharField(max_length=128, blank=True)
    email = models.CharField(unique=True, max_length=128, blank=True)
    phone = models.CharField(max_length=10, blank=True)

    class Meta:
        # managed = False
        db_table = 'persons'


class User(models.Model):
    auth_user = models.OneToOneField(User)
    user_name = models.CharField(primary_key=True, max_length=24)
    password = models.CharField(max_length=24, blank=True)
    class_field = models.CharField(db_column='class', max_length=1, blank=True)  # Field renamed because it was a Python reserved word.
    person = models.ForeignKey(Person, blank=True, null=True)
    date_registered = models.DateField(blank=True, null=True, default=datetime.date.today)

    class Meta:
        # managed = False
        db_table = 'users'


class FamilyDoctor(models.Model):
    doctor = models.ForeignKey(Person, related_name='doctor')
    patient = models.ForeignKey(Person, related_name='patient')

    class Meta:
        # managed = False
        db_table = 'family_doctor'


class PacsImage(models.Model):
    record = models.ForeignKey('RadiologyRecord')
    image_id = models.IntegerField(primary_key=True)
    thumbnail = models.TextField(blank=True)
    regular_size = models.TextField(blank=True)
    full_size = models.TextField(blank=True)

    class Meta:
        # managed = False
        db_table = 'pacs_images'

class RadiologyRecord(models.Model):
    record_id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(Person, blank=True, null=True, related_name='patient_r')
    doctor = models.ForeignKey(Person, blank=True, null=True, related_name='doctor_r')
    radiologist = models.ForeignKey(Person, blank=True, null=True, related_name='radiologist')
    test_type = models.CharField(max_length=24, blank=True)
    prescribing_date = models.DateField(blank=True, null=True, default=datetime.date.today)
    test_date = models.DateField(blank=True, null=True)
    diagnosis = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=1024, blank=True)

    class Meta:
        # managed = False
        db_table = 'radiology_record'
